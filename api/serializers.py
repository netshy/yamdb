from rest_framework import serializers
from .models import User, Category, Genre, Title, Comment, Review


class UserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'role', 'email', 'first_name', 'last_name', 'bio')


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleSlugSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(many=True, slug_field='slug', queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = '__all__'


class TitleGeneralSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategoriesSerializer()
    rating = serializers.FloatField()

    class Meta:
        model = Title
        fields = '__all__'


class UserInfoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'role', 'email', 'first_name', 'last_name', 'bio')


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    score = serializers.IntegerField(min_value=1, max_value=10)

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        user = self.context['request'].user
        if self.context['request'].method == 'PATCH':
            return data
        is_review_exists = Review.objects.filter(title=title_id, author=user).exists()
        if is_review_exists:
            raise serializers.ValidationError('Вы уже оставили отзыв.')
        return data

    class Meta:
        model = Review
        fields = ('id', 'pub_date', 'author', 'text', 'score')
        read_only_fields = ('id', 'pub_date', 'author')


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'pub_date', 'author')
