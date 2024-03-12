from typing_extensions import Awaitable
from fastapi import FastAPI, Depends
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent
from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from fastapi.responses import HTMLResponse
from typing import Annotated, Iterable, Generator
from fastui.forms import FormFile, SelectSearchResponse, Textarea, fastui_form
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import Session

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class UserTable(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    mail = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


#Base.metadata.create_all(engine, checkfirst=False)


def get_users(session: Session) -> list[UserTable]:
    return session.query(UserTable).all()


def get_user(session: Session, mail: str) -> UserTable:
    return session.query(UserTable).where(UserTable.mail == mail).one()


def add_user(session: Session, mail: str, password: str) -> None:
    session.add(UserTable(mail=mail, hashed_password=password))
    session.commit()


app = FastAPI()


class User(BaseModel):
    id: int
    mail: str
    hashed_password: str

    model_config = ConfigDict(
            from_attributes=True
        )

def get_session() -> Session:
    return SessionLocal()


@app.get("/api/users/", response_model=FastUI, response_model_exclude_none=True)
def users_table(session: Session = Depends(get_session)) -> list[AnyComponent]:
    users = [User.from_orm(user) for user in get_users(session)]
    return [
        c.Page(
            components=[
                c.Heading(text="Users", level=2),
                c.Table(
                    data=users,
                    columns=[
                        DisplayLookup(field="mail"),
                        DisplayLookup(field="hashed_password"),
                    ],
                ),
            ]
        ),
    ]


class LoginForm(BaseModel):
    mail: str
    password: str


@app.get("/api/login", response_model=FastUI, response_model_exclude_none=True)
def form_content():
    return [
        c.Heading(text="Login Form", level=2),
        c.Paragraph(text="Simple login form with email and password."),
        c.ModelForm(model=LoginForm, display_mode="page", submit_url="/api/login"),
    ]


@app.post("/api/login", response_model=FastUI, response_model_exclude_none=True)
def user_login(
    form: Annotated[LoginForm, fastui_form(LoginForm)],
    session: Session = Depends(get_session),
) -> list[AnyComponent]:
    add_user(session, form.mail, form.password)
    return [c.FireEvent(event=GoToEvent(url="/"))]


@app.get("/{path:path}")
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title="FastUI Demo"))
