from articles.models import Article
from orders.models import Order, OrderArticle, OrderEquipment
from stock.models import Equipment


def pack(order: Order):
    order_articles = OrderArticle.objects.filter(order=order)
    box = Equipment.objects.get(id=1)
    tube = Equipment.objects.get(id=2)
    box_count = 0
    tube_items_count = 0
    current_box_height = 0
    weight = 0
    # dimensions
    height = 0
    width = box.width
    length = box.length

    for order_item in order_articles:
        if order_item.article.geometry == Article.Geometries.BOX.value:
            if box_count == 0:
                box_count += 1
            for x in range(order_item.quantity):
                if current_box_height > box.height:
                    current_box_height = order_item.article.height
                    box_count += 1
                current_box_height += order_item.article.height
        elif order_item.article.geometry == Article.Geometries.TUBE.value:
            tube_items_count += 1
        weight += order_item.article.weight

    OrderEquipment.objects.create(order=order, equipment=box, quantity=box_count)
    weight += box_count * box.weight
    height += box_count * box.height

    if tube_items_count:
        if box_count == 0:
            width = tube.width
        if tube_items_count > 7:
            tube_count = tube_items_count // 7
            if tube_items_count % 7 > 0:
                tube_count += 1
        else:
            tube_count = 1

        OrderEquipment.objects.create(order=order, equipment=tube, quantity=tube_count)
        weight += tube_count * tube.weight
        height += tube_count * tube.height
        length = tube.length

    order.height = height
    order.width = width
    order.length = length
    order.weight = weight
    order.save()

