from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.core.database.database import get_session
from fast_zero.core.security import get_current_user
from fast_zero.models.models import Todo, User
from fast_zero.schemas.schemas import (
    FilterTodo,
    TodoList,
    TodoPublic,
    TodoSchema,
    TodoUpdate,
)

router = APIRouter(prefix='/todos', tags=['todos'])

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
FilterTodo = Annotated[FilterTodo, Query()]


@router.post('/', response_model=TodoPublic)
def create_todo(todo: TodoSchema, user: CurrentUser, session: Session):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.get('/', response_model=TodoList)
def get_all_todos(
    todos_filters: FilterTodo, user: CurrentUser, session: Session
):
    query = select(Todo).where(Todo.user_id == user.id)

    if todos_filters.title:
        query = query.filter(Todo.title.contains(todos_filters.title))

    if todos_filters.description:
        query = query.filter(
            Todo.description.contains(todos_filters.description)
        )

    if todos_filters.state:
        query = query.filter(Todo.state == todos_filters.state)

    todos = session.scalars(
        query.offset(todos_filters.offset).limit(todos_filters.limit)
    ).all()

    return {'todos': todos}


@router.patch('/{todo_id}', response_model=TodoPublic)
def patch_todo(
    todo_id: int, user: CurrentUser, session: Session, todo: TodoUpdate
):
    db_todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.delete('/{todo_id}')
def delete_todo(todo_id: int, user: CurrentUser, session: Session):
    db_todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    session.delete(db_todo)
    session.commit()

    return {'message': 'Task has been deleted successfully.'}
