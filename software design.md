### service responsibilities

root: /media_api/;

#### post 
- POST session/

#### comments 

### db
  ###### post
  ```json
  {
    "user_id": 291419, 
    "id": 345624,
    "topics": ["developer", "code", "money"],
    "body": "......",
    "images": ["fwd2hi4h3", "hufei724h2h3"],
    "timestamp": "utc-time"
  }
  ```

  ###### comment
  ```json
  {
    "user_id": 291419, 
    "post_id": 43253,
    "id": 324,
    "body": "......",
    "timestamp": "utc-time"
  }
  ```

  ###### likes 
  ```json
  {
    "user_id": 291419,
    "post_id": 43253,
    "comment_id": 253,
    "like": 1,
    "timestamp": "utc-time"
  }
  ```