# Lecture 6: Designing ER Model of Facebook

Goal: design the Facebook database as an ER diagram (conceptual schema), using the same 3 steps as the last lecture: identify entity sets, identify relationships, identify constraints. Only basic Facebook functions are used (no pages, reels, ads).

## Features and use cases

1. Profiles (user profiles): anyone who signs up becomes a user.
2. A user has friends; the friends are themselves users. Keep this in mind: it is a relationship between users and users.
3. A user can post. A post has text content, and also images, videos and so on.
4. A post can be liked and commented on by users.
5. Friends can visit your timeline and see all your posts. Implemented with the database: visiting a timeline extracts all posts of that profile from the database, retrieves them and shows them on the timeline.

## Step 1: Identify entity sets

1. User Profile
2. User Post
3. Post Comment (comments on a post)
4. Post Like (likes on a post)

- A post can have many likes and many comments, so likes and comments are stored as separate entities, not inside the post.
- Why not make Likes an attribute of Post: many different users make the likes (same for comments), so a relationship would be hard to establish. In an ER model a relationship exists between two entities, never between an attribute and an entity. So Post and Like are broken into two entities.
- While building an ER diagram or any schema, you often find wrong assumptions or mistakes later and go back and refine the DB schema. This happens in the real world too.
- Practice with many ER diagrams makes this kind of thinking clear.

## Attribute types

1. User Profile: Name, Email, Password, Contact Number, Date of Birth, Age
   - Name: composite
   - User Name: primary key
   - Email: can be multi-valued (multiple emails stored). Multi-valued or not depends on the requirement.
   - Contact Number: multi-valued
   - Age: derived (computed from Date of Birth)
2. User Post: Post ID, Content, Images, Videos, Created Time, Modified Time
   - Post ID: unique identification, primary key
   - Content: text
   - Images: multi-valued (a post can have multiple images)
   - Videos: multi-valued
   - Created Time: when the post was created
   - Modified Time: Facebook later got a modification feature, so it is added
3. Post Comment: Post Comment ID
   - Post Comment ID: used for unique identification, primary key

## Step 2: Identify relationships and constraints

1. User Profile - Friendship - User Profile
   - A relationship between one user profile and another user profile.
   - Mapping cardinality: M:N. One user profile can be a friend of many users, and one friend can be a friend of many user profiles.
2. User Profile - Posts - User Post
   - A user profile posts (not "shares") a post.
   - Participation: total on the User Post side. Every post is posted by some user profile; there is no orphan post.
   - Cardinality: 1:N. One user can post N posts.
3. User Profile - Likes - User Post
   - A user profile can like a post.
   - Mapping cardinality: one user profile can like N posts, but a given Like is not made by N users, so 1:N.
   - Participation: total for Post Like. Any like on a post was made by some user profile.
4. User Profile - Comments - Post Comment
   - One user profile can comment N times; one comment is made by exactly one user profile. Cardinality 1:N.
   - Participation: total for Post Comment. A comment is made by some user profile.
5. User Post - Has - Post Comment
   - One user post can have N comments. Cardinality 1:N.
   - Participation: total for Post Comment. Any comment is on some user post.
6. User Post - Has - Post Like
   - One user post can have N likes. Cardinality 1:N.
   - Participation: total for Post Like. Any like is associated with some user post.

Total: 6 relationships. The same 3 steps were used: entity sets (4 identified), relationships and constraints.

## Final ER diagram (conceptual schema)

- User Profile: Name (composite), User Name (primary key), Email (multi-valued), Password, Contact Number (multi-valued), Age (derived).
- Friendship: User Profile to User Profile, M:N.
- User Profile - Posts - User Post: 1:N, total participation on User Post.
- User Profile - Comments - Post Comment: 1:N, total participation on Post Comment.
- User Post: Post ID (primary key), Content, Images (multi-valued), Videos (multi-valued), Created Time, Modified Time.
- User Post - Has - Post Comment: 1:N, total participation on Post Comment.
- User Post - Has - Post Like: 1:N, total participation on Post Like.
- User Profile - Likes - Post Like: 1:N, total participation on Post Like.

## Viewer question: Likes as an attribute of User Post

- If Likes were made an attribute of User Post, the User Profile - Like relationship could not be established. That is why Like is its own entity.
- Thinking this way comes only from practice.
- Next lecture: the relational model, and how to convert an ER diagram into a relational model.
