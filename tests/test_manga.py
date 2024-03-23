# bilibili_api.manga

from bilibili_api import manga

from .common import get_credential

comic = manga.Manga(manga_id=30023, credential=get_credential())


async def test_a_Manga_get_info():
    return await comic.get_info()


async def test_b_Manga_get_images_url():
    return await comic.get_images_url(1)


# async def test_c_Manga_get_images():
#     return await comic.get_images(1)


async def test_d_set_follow_manga():
    print()
    print("正在设置追漫...")
    await manga.set_follow_manga(manga=comic, status=True)
    print("正在取消追漫...")
    await manga.set_follow_manga(manga=comic, status=False)


async def test_e_get_manga_index():
    return await manga.get_manga_index(credential=get_credential())


async def test_f_get_manga_update():
    return await manga.get_manga_update(credential=get_credential())


async def test_g_get_manga_home_recommend():
    return await manga.get_manga_home_recommend(credential=get_credential())
