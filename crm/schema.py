import graphene
from crm.models import Product

class UpdateLowStockProducts(graphene.Mutation):
    success = graphene.String()
    updated = graphene.List(graphene.String)

    def mutate(self, info):
        updated_products = []
        for product in Product.objects.filter(stock__lt=10):
            product.stock += 10
            product.save()
            updated_products.append(f"{product.name} - new stock {product.stock}")

        return UpdateLowStockProducts(success="Stock updated!", updated=updated_products)

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()
