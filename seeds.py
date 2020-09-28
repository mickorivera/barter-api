import logging
import os

from app.constants import UserRole
from app.v1.card.models import CardModel
from app.v1.comment.models import CommentModel, CommentReplyModel
from app.v1.list.models import ListModel
from app.v1.user.models import UserModel
from app.utils.hashing import get_hash

logging.basicConfig(level=logging.INFO)


def clear_table():
    UserModel.truncate_table(cascade=True)


def seed():
    salt = os.urandom(32)
    password = "qwerty"

    micko = UserModel.create(
        username="micko",
        email_address="micko@gmail.com",
        salt=salt,
        key=get_hash(password=password, salt=salt),
        role=UserRole.ADMIN,
    )
    logging.info(f"Created {micko.username}")

    michael = UserModel.create(
        username="michael",
        email_address="michael@gmail.com",
        salt=salt,
        key=get_hash(password=password, salt=salt),
        role=UserRole.ADMIN,
    )
    logging.info(f"Created {michael.username}")

    angelo = UserModel.create(
        username="angelo",
        email_address="angelo@gmail.com",
        salt=salt,
        key=get_hash(password=password, salt=salt),
    )
    logging.info(f"Created {angelo.username}")

    rivera = UserModel.create(
        username="rivera",
        email_address="rivera@gmail.com",
        salt=salt,
        key=get_hash(password=password, salt=salt),
    )
    logging.info(f"Created {rivera.username}")

    for admin in (micko, michael):
        for list_index in range(2):
            app_list = ListModel.create(
                author=admin, title=f"{admin.username} list {list_index}"
            )
            logging.info(f"{admin.username} created {app_list.title}")

            for card_index in range(3):
                card = CardModel.create(
                    author=admin,
                    list=app_list,
                    title=f"{app_list.title} Card {card_index}",
                    description=f"{app_list.title} Card {card_index} Description",
                )
                logging.info(
                    f"{admin.username} created {card.title} on {app_list}"
                )

                for comment_index in range(5):
                    comment = CommentModel.create(
                        author=admin,
                        card=card,
                        content=f"{card.title} Comment {comment_index}",
                    )
                    logging.info(
                        f"{admin.username} commented {comment.content} on {card.title}"
                    )

                    for reply_index in range(5):
                        comment_reply = CommentReplyModel.create(
                            author=admin,
                            comment=comment,
                            content=f"{comment.content} Comment Reply {reply_index}",
                        )
                        logging.info(
                            f"{admin.username} commented {comment_reply.content} on {comment.content}"
                        )


if __name__ == "__main__":
    clear_table()
    seed()
