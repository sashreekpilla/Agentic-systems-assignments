from pydantic import BaseModel, Field, ValidationError
from sqlalchemy import create_engine, select
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, sessionmaker
from typing import Optional


# Create the declarative base — parent for all ORM table classes
Base = declarative_base()


# ORM class that maps to the products table in SQLite
class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    category: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
    in_stock: Mapped[bool] = mapped_column()


engine = create_engine("sqlite:///gadgetmart.db", echo=False)
Base.metadata.create_all(engine)

# Session factory bound to our engine — each session is one conversation with the DB
SessionLocal = sessionmaker(bind=engine)


SAMPLE_PRODUCTS = [
    {"name": "iPhone 15", "category": "mobile", "price": 79900, "in_stock": True},
    {"name": "Samsung Galaxy S24", "category": "mobile", "price": 74999, "in_stock": True},
    {"name": "OnePlus 12R", "category": "mobile", "price": 42999, "in_stock": True},
    {"name": "Google Pixel 8", "category": "mobile", "price": 54999, "in_stock": False},
    {"name": "Redmi Note 13", "category": "mobile", "price": 18999, "in_stock": True},
    {"name": "Motorola Edge 40", "category": "mobile", "price": 29999, "in_stock": True},
]


class ProductSearchInput(BaseModel):
    category: str = Field(..., min_length=1)
    max_price: int = Field(..., gt=0)
    in_stock: Optional[bool] = True


def insert_data() -> None:
    """Insert demo products if you are running the script fresh."""
    # Open a short-lived database session
    with SessionLocal() as session:
        products = [Product(**row) for row in SAMPLE_PRODUCTS]
        session.add_all(products)
        session.commit()


def search_product(input_data: dict):
    """
    Tool function: validate dict input, query ORM, return rows or an error dict.
  """
    try:
        validated_input = ProductSearchInput(**input_data)
    except ValidationError as err:
        return {
            "success": False,
            "error": "Invalid input provided",
            "details": err.errors(),
        }

    # New session for the read query
    with SessionLocal() as session:
        query = select(Product).where(
            Product.category == validated_input.category,
            Product.price <= validated_input.max_price,
            Product.in_stock == validated_input.in_stock,
        )

        products_from_db = session.scalars(query).all()
        return products_from_db


def agent_flow() -> None:
    """
    Simulated agent step: one hard-coded tool call instead of live LLM routing.
  """
    tool_calls = [
        {
            "tool_name": "search_product_tool",
            "arguments": {
                "category": "mobile",
                "max_price": 50000,
                "in_stock": True,
            },
        }
    ]

    for tool_call in tool_calls:
        arguments = tool_call["arguments"]
        tool_output = search_product(arguments)

        for tool in tool_output:
            print (f"{tool.name} - {tool.price}")


if __name__ == "__main__":
    # insert_data()
    agent_flow()
