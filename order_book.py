from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models import Base, Order
engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def process_order(order_data):
    # Step 1: Insert the new order into the database
    new_order = Order(
        buy_currency=order_data['buy_currency'],
        sell_currency=order_data['sell_currency'],
        buy_amount=order_data['buy_amount'],
        sell_amount=order_data['sell_amount'],
        sender_pk=order_data['sender_pk'],
        receiver_pk=order_data['receiver_pk']
    )
    session.add(new_order)
    session.commit()

    # Step 2: Match existing orders and create child orders if needed
    matching_orders = session.query(Order).filter(
        Order.filled.is_(None),
        Order.buy_currency == order_data['sell_currency'],
        Order.sell_currency == order_data['buy_currency'],
        (Order.sell_amount * order_data['sell_amount']) >= (Order.buy_amount * order_data['buy_amount'])
    ).all()
    session.commit()

    for existing_order in matching_orders:
        if existing_order.sell_amount == order_data['buy_amount']:
            # Exact match, both orders completely filled
            existing_order.filled = datetime.now()
            new_order.filled = datetime.now()
            existing_order.counterparty_id = new_order.id
            new_order.counterparty_id = existing_order.id
            session.commit()
            break

        elif existing_order.sell_amount > order_data['buy_amount']:
            # Existing order partially filled, create child order
            existing_order.filled = datetime.now()
            new_order.filled = datetime.now()
            existing_order.counterparty_id = new_order.id
            new_order.counterparty_id = existing_order.id

            # Create a child order for the remaining balance
            child_sell_amount = (existing_order.buy_amount - order_data['sell_amount'])* (existing_order.sell_amount/existing_order.buy_amount )

            child_order = Order(
                buy_currency=existing_order.buy_currency,
                sell_currency=existing_order.sell_currency,
                buy_amount=existing_order.buy_amount - order_data['sell_amount'],
                sell_amount=child_sell_amount,
                sender_pk=existing_order.sender_pk, 
                receiver_pk=existing_order.receiver_pk
            )

            child_order.creator_id = existing_order.id  # Set the creator of the child order
            session.add(child_order)
            session.commit()
            break
        
        else existing_order.sell_amount < order_data['buy_amount']:
            # Existing order fully filled, create child order for new order
            existing_order.filled = datetime.now()
            new_order.filled = datetime.now()
            existing_order.counterparty_id = new_order.id
            new_order.counterparty_id = existing_order.id

            # Create a child order for the remaining balance
            child_sell_amount = (order_data['buy_amount'] - existing_order.sell_amount)* (order_data['sell_amount']/order_data['buy_amount'] )

            child_order = Order(
                buy_currency=order_data.buy_currency,
                sell_currency=order_data.sell_currency,
                buy_amount=order_data['buy_amount'] - existing_order.sell_amount,
                sell_amount=child_sell_amount,
                sender_pk=order_data['sender_pk'], 
                receiver_pk=order_data['receiver_pk']
            )

            child_order.creator_id = order_data.id  # Set the creator of the child order
            session.add(child_order)
            session.commit()
            break


    # Commit changes to the database
    session.commit()

    pass
