from djangochannelsrestframework import permissions
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import ListModelMixin
from djangochannelsrestframework.observer import model_observer

from .models import ItemBorrow
from .serializers import ItemBorrowSerializer

class ItemBorrowConsumer(ListModelMixin, GenericAsyncAPIConsumer):

    queryset = ItemBorrow.objects.all()
    serializer_class = ItemBorrowSerializer
    permission = (permissions.AllowAny)

    async def connect(self, **kwargs):
        await self.model_change.subscribe()
        await super().connect()
    
    @model_observer(ItemBorrow)
    async def model_change(self, message, observer=False, **kwargs):
        await self.send_json(message)
    
    @model_change.serializer
    def model_serializer(self, instance, action, **kwargs):
        return dict(data = ItemBorrowSerializer(instance=instance).data, action=action.value)