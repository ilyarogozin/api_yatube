from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from posts.models import Comment, Group, Post, Follow, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    def validate_following(self, following):
        """
        Checks that you are not subscribing to yourself.
        Checks that the subscription does not exist yet.
        """
        user = self.context['request'].user
        if following == user:
            raise serializers.ValidationError(
                'Вы не можете подписаться сами на себя!'
            )
        elif Follow.objects.filter(following=following, user=user).exists:
            raise serializers.ValidationError('Такая подписка уже существует!')
        return following

    class Meta:
        model = Follow
        fields = '__all__'
        read_only_fields = ('user',)
