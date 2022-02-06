import os
import random

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from petstagram import settings
from petstagram.accounts.models import Profile
from petstagram.pets.models import Pet
from petstagram.tests.base.tests import PetstagramTestCase


class ProfileDetailsTest(PetstagramTestCase):

    def test_getDetails_whenLogedInUserWithNoPets_shouldGetDetailsWithNoPets(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("profile details"))

        pets = list(response.context["pets"])
        profile = response.context["profile"]

        self.assertListEmpty(pets)
        self.assertEqual(self.user.id, profile.user.id)

    def test_getDetails_whenLogedInUserWithPets_shouldGetDetailsWithPets(self):
        pet = Pet.objects.create(
            name="Test",
            description="Test pet description",
            age=1,
            image='path/to/image.png',
            type=Pet.TYPE_CHOICE_DOG,
            user=self.user
        )
        self.client.force_login(self.user)
        response = self.client.get(reverse("profile details"))

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.user.id, response.context["profile"].user_id)
        self.assertListEqual([pet], list(response.context["pets"]))

    def test_postDetails_whenUserLoggedInWithoutImage_shouldChangeImage(self):
        path_to_image = os.path.join(settings.BASE_DIR, 'tests', 'media', 'test_image.webp')
        file_name = f'{random.randint(1, 10000)}-test_image.webp'
        file = SimpleUploadedFile(
            name=file_name,
            content=open(path_to_image, 'rb').read(),
            content_type='image/jpeg')

        self.client.force_login(self.user)

        response = self.client.post(reverse('profile details'), data={
            'profile_image': file,
        })

        self.assertEqual(302, response.status_code)

        profile = Profile.objects.get(pk=self.user.id)
        self.assertTrue(str(profile.profile_image).endswith(file_name))


# def test_postDetails_whenUserLoggedInWithImage_shouldChangeImage(self):
#     path_to_image = 'path/to/image.png'
#     profile = Profile.objects.get(pk=self.user.id)
#     profile.profile_image = path_to_image + 'old'
#     profile.save()
#
#     self.client.force_login(self.user)
#
#     response = self.client.post(reverse('profile details'), data={
#         'profile_image': path_to_image,
#     })
#
#     self.assertEqual(302, response.status_code)
#
#     profile = Profile.objects.get(pk=self.user.id)
