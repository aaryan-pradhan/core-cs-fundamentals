# 8. REST APIs and Blob Storage

## REST protocol

The client talks to the server over HTTP using REST. Each request names a **method** and a **path**. The server replies with a **status code** and a body, usually JSON.

```mermaid
flowchart LR
    C["Client"] -->|"GET /count<br/>POST /increment"| LB["Load Balancer"]
    LB -->|"forward"| A["App Server"]
    A -->|"200 OK {count: 2}"| LB
    LB -->|"200 OK {count: 2}"| C
```

| Method | Meaning | Example |
|--------|---------|---------|
| GET | Read a resource. No side effects. | `GET /count` |
| POST | Create something or trigger an action | `POST /increment` |
| PUT | Replace a resource | `PUT /users/42` |
| PATCH | Change part of a resource | `PATCH /count` |
| DELETE | Remove a resource | `DELETE /files/7` |

| Status code | Meaning |
|-------------|---------|
| 200 OK | Success |
| 201 Created | A new resource was made |
| 204 No Content | Success with no body |
| 301 / 302 | Redirect (permanent / temporary) |
| 400 Bad Request | The input is wrong |
| 401 Unauthorized | Not logged in |
| 403 Forbidden | Logged in, but not allowed |
| 404 Not Found | The resource does not exist |
| 429 Too Many Requests | Rate limit hit |
| 500 Internal Server Error | The server failed |

## The problem: uploading a file through the app server

A naive upload API puts the file inside the JSON body:

```
GET  /file/{name}
POST /file
body: {
  "name": "study.pdf",
  "data": "ksdhkf7983u2rnfkjsy89u23oif9y2oho...."   // 2 GB!
}
```

The 2 GB travels from the client to the LB, then to the app server, then to the database. Every hop carries the full file. This bloats the servers and the DB.

## Blob store

A **blob store** (Binary Large OBject store) stores and returns large unstructured files as objects (blobs). Examples: images, videos, PDFs, audio, backups, ZIPs, ML datasets.

| | Database | Blob store |
|---|----------|------------|
| Best for | Structured records and queries | Files |
| Operations | Tables, indexes, joins | PUT object, GET object, DELETE object, LIST objects |
| Examples | Postgres, MySQL | Amazon S3, Cloudflare R2, Google Cloud Storage (GCS) |

- **Rule:** Store the file in the blob store. Store only its metadata (owner, key, size, type) in the DB.

## Pre-signed URL

A **pre-signed URL** is a link to one object in the blob store. It carries a signature and an expiry time. Anyone with the link can do one action (PUT or GET) on that one object until it expires.

- **No network call:** The app server creates the URL in its own memory. It signs it with its cloud credentials. The blob store checks the signature later.
- **Short life:** It is valid for a short time, for example 5 to 15 minutes.

Example:

```
https://my-bucket.s3.ap-south-1.amazonaws.com/users/42/uploads/9f3c2b1e-resume.pdf
?X-Amz-Algorithm=AWS4-HMAC-SHA256
&X-Amz-Credential=AKIAIOSFODNN7EXAMPLE%2F20260205%2Fap-south-1%2Fs3%2Faws4_request
&X-Amz-Date=20260205T120000Z
&X-Amz-Expires=900
&X-Amz-SignedHeaders=host%3Bcontent-type
&X-Amz-Signature=0123456789abcdef...
```

| Part | Meaning |
|------|---------|
| Path | The object key: `users/42/uploads/9f3c2b1e-resume.pdf` |
| `X-Amz-Algorithm` | The signing algorithm |
| `X-Amz-Credential` | Which access key signed it, the date, region and service |
| `X-Amz-Date` | When it was signed |
| `X-Amz-Expires` | Seconds it stays valid: 900 = 15 minutes |
| `X-Amz-SignedHeaders` | Headers the request must match |
| `X-Amz-Signature` | The signature the blob store verifies |

## Upload flow

The file goes straight from the client to the blob store. It is uploaded only once.

```mermaid
flowchart LR
    C["Client"] -->|"1. POST /uploads/init"| A["App Server"]
    A -->|"2. uploadUrl + objectKey"| C
    C -->|"3. PUT file bytes once<br/>(2 GB)"| S3[("Blob store (S3)")]
    C -->|"4. POST /uploads/complete"| A
    A -->|"5. INSERT metadata"| D[("Database")]
```

```mermaid
sequenceDiagram
    actor U as User
    participant F as Frontend (Browser)
    participant B as Backend API
    participant S as Blob Store (S3/R2/GCS)
    participant D as Database (metadata)
    U->>F: Select file (resume.pdf)
    F->>B: POST /uploads/init {name, size, contentType}
    B->>B: Auth + validate (size, type, quota)
    B->>S: Create pre-signed PUT URL (key, expiry)
    S-->>B: preSignedPutUrl + objectKey
    B-->>F: 200 {uploadUrl, objectKey}
    F->>S: PUT uploadUrl (file bytes + Content-Type)
    S-->>F: 200/204 OK (ETag)
    F->>B: POST /uploads/complete {objectKey, etag}
    B->>D: INSERT file metadata (user_id, key, size, type, etag)
    D-->>B: OK
    B-->>F: 200 {fileId}
```

1. **Init:** The frontend calls `POST /uploads/init` with `filename`, `size` and `contentType`.
2. **Auth and validate:** The backend checks: Is the user logged in? Are the file size and type allowed? Is the user within rate limits and quota?
3. **Pre-signed PUT URL:** The backend makes an object key like `users/42/resumes/uuid-resume.pdf`. It creates a pre-signed URL valid for 5 to 15 minutes. It returns `uploadUrl`, `objectKey` and sometimes required headers.
4. **Direct upload:** The frontend sends the bytes to `uploadUrl`. The blob store replies with an **ETag**, a fingerprint of the stored file.
5. **Complete:** The frontend calls `POST /uploads/complete`. The backend saves the metadata row and returns `fileId`.

## Download flow

```mermaid
sequenceDiagram
    actor U as User
    participant F as Frontend (Browser)
    participant B as Backend API
    participant S as Blob Store (S3/R2/GCS)
    participant D as Database (metadata)
    U->>F: Click "Download"
    F->>B: GET /files/{fileId}/download
    B->>D: SELECT metadata WHERE id = fileId
    D-->>B: {objectKey, owner, contentType, filename}
    B->>B: AuthZ check (owner / ACL)
    B->>S: Create pre-signed GET URL (key, expiry, Content-Disposition)
    S-->>B: preSignedGetUrl
    B-->>F: 200 {downloadUrl}
    F->>S: GET downloadUrl
    S-->>F: 200 (file bytes)
    F-->>U: Browser saves or opens the file
```

- **ACL:** Access control list. It says who may read the file.
- **Content-Disposition:** A header that tells the browser to download the file and what to name it.

> **Interview:** Never send large files through your app servers. Use a blob store with pre-signed URLs. Keep metadata in the DB.
