from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int]
    name: Mapped[str | None]
    surname: Mapped[str | None]


class Schedule(Base):
    __tablename__ = "schedule"

    lesson: Mapped[str]
    format: Mapped[str]
    date: Mapped[str]
    hours: Mapped[str]
    minutes: Mapped[str]
    users_number: Mapped[int]
    additional_info: Mapped[str]
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class Practice(Base):
    __tablename__ = "practices"

    user_id: Mapped[int]
    lessons: Mapped[str]
    format: Mapped[str]
    date: Mapped[str]
    hours: Mapped[str]
    minutes: Mapped[str]
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class LessonTitle(Base):
    __tablename__ = "lessons_title"

    title: Mapped[str]
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class QuitedPractice(Base):
    __tablename__ = "quited_practice"

    practice: Mapped[str]
    reason: Mapped[str]
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class LastBotMessage(Base):
    __tablename__ = "last_bot_message"

    user_id: Mapped[int]
    message_number: Mapped[int]
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class WorkshopsSchedule(Base):
    __tablename__ = "workshops_schedule"

    title: Mapped[str]
    format: Mapped[str]
    date: Mapped[str]
    hours: Mapped[str]
    minutes: Mapped[str]
    users_number: Mapped[int]
    additional_info: Mapped[str]
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class Workshop(Base):
    __tablename__ = "workshops"

    user_id: Mapped[int]
    title: Mapped[str]
    format: Mapped[str]
    date: Mapped[str]
    hours: Mapped[str]
    minutes: Mapped[str]
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class WorkshopTitle(Base):
    __tablename__ = "workshops_title"

    title: Mapped[str]
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class QuitedWorkshop(Base):
    __tablename__ = "quited_workshops"

    workshop: Mapped[str]
    reason: Mapped[str]
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
