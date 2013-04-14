# richard -- video index system
# Copyright (C) 2012, 2013 richard contributors.  See AUTHORS.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# TODO: Write more

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.template.loader import get_template
from django.template.base import TemplateDoesNotExist

from nose.tools import eq_

from richard.videos.feeds import CategoryFeed
from richard.videos.models import Video
from richard.videos.tests import category, video, speaker


class FeedTest(TestCase):

    def test_category_feed(self):
        """Tests for Category rss feed"""

        # Test that only categories with live videos are included."""
        feed = CategoryFeed()

        cat = category(save=True)
        v1 = video(category=cat, save=True)
        v2 = video(category=cat, save=True)

        # No live videos, no category in feed
        eq_(len(feed.items()), 0)

        # At least one video is live, category is included
        v2.state = Video.STATE_LIVE
        v2.save()
        eq_([x.pk for x in feed.items()], [cat.pk])

        # Category feed description_template exists.
        found_tpl = True
        try:
            tpl = get_template(feed.description_template)
        except TemplateDoesNotExist:
            found_tpl = False
        eq_(found_tpl, True)

        # Category list feeds is accessible.
        resp = self.client.get(reverse('videos-category-feed'))
        eq_(resp.status_code, 200)

        # Category videos feed is accessible.
        resp = self.client.get(reverse(
                        'videos-category-videos-feed', 
                        kwargs={'category_id': cat.id, 'slug': cat.slug,}))
        eq_(resp.status_code, 200)

        # Category videos feed returns 404, invalid category_id.
        resp = self.client.get(reverse(
                        'videos-category-videos-feed', 
                        kwargs={'category_id': 50, 'slug': 'fake-slug',}))
        eq_(resp.status_code, 404)

    def test_speaker_feed(self):
        """Tests for Speaker rss feed"""

        spk = speaker(save=True)

        # Speaker feed is accessible
        resp = self.client.get(reverse(
                        'videos-speaker-feed',
                        kwargs={'speaker_id': spk.id, 'slug': spk.slug,}))
        eq_(resp.status_code, 200)

        # Speaker feed returns 404, invalid speaker_id.
        resp = self.client.get(reverse(
                        'videos-speaker-feed',
                        kwargs={'speaker_id': 50, 'slug': 'fake-slug',}))
        eq_(resp.status_code, 404)

    def test_video_feed(self):
        """Tests for Video rss feed"""

        #Video feed is accessible
        resp = self.client.get(reverse('videos-new-feed'))
        eq_(resp.status_code, 200)



