from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

from . import service
from .dependencies import get_db
from .exceptions import InitializeNonExistingStore, StoreNotFound
from .schemas import Store, StoreInitialize

router = APIRouter()


@router.get("/{seller_id}", response_model=Store)
def read_store(seller_id: UUID4, database: Session = Depends(get_db)):
    store = service.get_store_by_user_id(database, seller_id)

    if store is None:
        raise StoreNotFound

    return store


@router.put("/{seller_id}", response_model=Store)
def update_store(seller_id: UUID4, store: StoreInitialize, database: Session = Depends(get_db)):
    seller = service.get_store_by_user_id(database, seller_id)

    if seller is None:
        raise InitializeNonExistingStore

    updated_store = service.update_store(database, seller_id, store)

    return updated_store
