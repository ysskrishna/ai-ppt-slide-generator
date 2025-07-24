from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.dbutils import get_db
from typing import Optional

router = APIRouter()
