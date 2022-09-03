from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, models, database, oauth2
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/vote",
    tags=["vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()                # when we wanna vote a post that doesn't exist.
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id :{vote.post_id} doesn't exist")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)      # this is gonna check if the specific user already voted for a specific post.
    found_vote = vote_query.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")

        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)        # if the user previously didn't vote the post we create a brand new vote for that.
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"vote does not exist")         # if we want delete the vote of the post that doesn't have a vote we say...

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "vote successfully deleted"}


