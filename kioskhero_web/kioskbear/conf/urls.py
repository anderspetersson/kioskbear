from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from rest_framework import routers, serializers, viewsets

from kioskbear.accounts.models import Customer
from kioskbear.kiosk.models import Survey, Block
from kioskbear.feedback.models import Rating, Option, ScoredOption


class ScoredOptionSerializer(serializers.ModelSerializer):
    follow_up_block_id = serializers.PrimaryKeyRelatedField(source='follow_up_block', read_only=True)
    class Meta:
        model = ScoredOption
        fields = ['id', 'text', 'score', 'follow_up_block_id']


class OptionSerializer(serializers.ModelSerializer):
    follow_up_block_id = serializers.PrimaryKeyRelatedField(source='follow_up_block', read_only=True)
    class Meta:
        model = Option
        fields = ['id', 'text', 'follow_up_block_id']


class BlockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Block
        fields = ['id', 'title', 'options', 'scored_options']


class SurveySerializer(serializers.ModelSerializer):
    start_block = BlockSerializer(read_only=True)
    #block_set = BlockSerializer(many=True, read_only=True)
    end_block = BlockSerializer(read_only=True)

    class Meta:
        model = Survey
        fields = ['id', 'start_block', 'block_set', 'end_block']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'organisation_name']
        read_only_fields = ['id', 'organisation_name']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'survey', 'score']


class CustomerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class SurveyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer


class BlockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer

class ScoredOptionViewSet(viewsets.ModelViewSet):
    queryset = ScoredOption.objects.all()
    serializer_class = ScoredOptionSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'surveys', SurveyViewSet)
router.register(r'blocks', BlockViewSet)
router.register(r'ratings', RatingViewSet)
router.register(r'options', OptionViewSet)
router.register(r'scored-options', ScoredOptionViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('kioskbear.landingpages.urls', namespace='landingpages')),
    path('accounts/', include('kioskbear.accounts.urls', namespace='accounts')),
    path('app/', include('kioskbear.app.urls', namespace='app')),
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += staticfiles_urlpatterns()