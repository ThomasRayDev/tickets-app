from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from tickets import router as tickets_router

app = FastAPI()

origins = [
  'http://127.0.0.1:3000',
  'http://localhost:3000',
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)

app.include_router(auth_router, tags=['Auth'])
app.include_router(tickets_router, prefix='/tickets', tags=['Tickets'])
