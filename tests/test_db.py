import pytest

from fastapi_zero.models import User


@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    with mock_db_time() as time:
        user = User(
            username='test_user',
            email='test_user@example.com',
            password='securepassword',
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)

        assert user.id is not None
        assert user.username == 'test_user'
        assert user.email == 'test_user@example.com'
        assert user.password == 'securepassword'
        assert user.created_at == time
