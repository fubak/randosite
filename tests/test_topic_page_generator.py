#!/usr/bin/env python3
"""
Tests for topic_page_generator module.

Tests the modular functions for topic page generation.
"""

import pytest
from scripts.topic_page_generator import (
    get_topic_configurations,
    extract_headline_keywords,
    score_image_relevance,
    find_topic_hero_image,
    matches_topic_source,
    filter_trends_by_topic,
    get_topic_hero_image_from_story_or_search,
    should_generate_topic_page
)


class TestTopicConfigurations:
    """Tests for topic configuration retrieval."""

    def test_get_topic_configurations_returns_list(self):
        """Topic configurations should return a list."""
        configs = get_topic_configurations()
        assert isinstance(configs, list)
        assert len(configs) > 0

    def test_topic_config_structure(self):
        """Each topic config should have required fields."""
        configs = get_topic_configurations()
        required_fields = {'slug', 'title', 'description', 'source_prefixes', 'hero_keywords', 'image_index'}

        for config in configs:
            assert all(field in config for field in required_fields), \
                f"Config for {config.get('slug')} missing required fields"

    def test_topic_slugs_are_unique(self):
        """Topic slugs should be unique."""
        configs = get_topic_configurations()
        slugs = [c['slug'] for c in configs]
        assert len(slugs) == len(set(slugs)), "Duplicate topic slugs found"

    def test_tech_topic_exists(self):
        """Tech topic should be configured."""
        configs = get_topic_configurations()
        tech_configs = [c for c in configs if c['slug'] == 'tech']
        assert len(tech_configs) == 1
        assert 'hackernews' in tech_configs[0]['source_prefixes']


class TestKeywordExtraction:
    """Tests for headline keyword extraction."""

    def test_extract_basic_keywords(self):
        """Should extract meaningful keywords from headline."""
        headline = "Apple releases new iPhone with amazing camera features"
        keywords = extract_headline_keywords(headline)

        assert 'apple' in keywords
        assert 'releases' in keywords
        assert 'iphone' in keywords
        assert 'amazing' in keywords
        assert 'camera' in keywords
        assert 'features' in keywords

    def test_filters_stop_words(self):
        """Should filter out common stop words."""
        headline = "The company is releasing a new product for the market"
        keywords = extract_headline_keywords(headline)

        # Stop words should be removed
        assert 'the' not in keywords
        assert 'is' not in keywords
        assert 'a' not in keywords
        assert 'for' not in keywords

        # Content words should remain
        assert 'company' in keywords
        assert 'releasing' in keywords
        assert 'product' in keywords
        assert 'market' in keywords

    def test_filters_short_words(self):
        """Should filter out words with length <= 2."""
        headline = "AI is on the rise in tech"
        keywords = extract_headline_keywords(headline)

        assert 'ai' not in keywords  # Length 2
        assert 'is' not in keywords  # Stop word + length 2
        assert 'on' not in keywords  # Stop word + length 2
        assert 'in' not in keywords  # Stop word + length 2

        assert 'rise' in keywords
        assert 'tech' in keywords

    def test_handles_punctuation(self):
        """Should strip punctuation from keywords."""
        headline = "Breaking: Tech giant's new product!"
        keywords = extract_headline_keywords(headline)

        assert 'breaking' in keywords  # Colon removed
        assert 'tech' in keywords
        assert 'giant' in keywords  # Apostrophe-s removed (giant's → giant)
        assert 'product' in keywords  # Exclamation removed

    def test_handles_empty_headline(self):
        """Should handle empty headlines gracefully."""
        keywords = extract_headline_keywords("")
        assert keywords == []

    def test_case_insensitive(self):
        """Should convert to lowercase for consistency."""
        headline = "BREAKING NEWS: Major Announcement Today"
        keywords = extract_headline_keywords(headline)

        assert 'breaking' in keywords
        assert 'news' in keywords  # Not filtered as it's not in stop words
        assert 'major' in keywords
        assert 'announcement' in keywords


class TestImageScoring:
    """Tests for image relevance scoring."""

    def test_headline_keyword_match_scores_higher(self):
        """Headline keywords should score 2 points each."""
        image = {
            'query': 'technology innovation',
            'description': 'modern tech',
            'alt': 'innovation',
            'width': 1000
        }

        score = score_image_relevance(
            image,
            headline_keywords=['technology', 'innovation'],
            category_keywords=[]
        )

        # 'technology' (2) + 'innovation' (2) = 4
        assert score == 4.0

    def test_category_keyword_match_scores_lower(self):
        """Category keywords should score 1 point each."""
        image = {
            'query': 'business office',
            'description': 'corporate',
            'alt': 'meeting',
            'width': 1000
        }

        score = score_image_relevance(
            image,
            headline_keywords=[],
            category_keywords=['business', 'office', 'corporate']
        )

        # 'business' (1) + 'office' (1) + 'corporate' (1) = 3
        assert score == 3.0

    def test_large_image_gets_bonus(self):
        """Images >= 1200px should get 0.5 point bonus."""
        image_small = {'query': 'tech', 'description': '', 'alt': '', 'width': 800}
        image_large = {'query': 'tech', 'description': '', 'alt': '', 'width': 1200}

        score_small = score_image_relevance(image_small, ['tech'], [])
        score_large = score_image_relevance(image_large, ['tech'], [])

        assert score_large == score_small + 0.5

    def test_no_keyword_match_returns_zero(self):
        """No keyword matches should return 0 (or 0.5 for large image)."""
        image_small = {'query': 'random', 'description': 'unrelated', 'alt': 'other', 'width': 800}
        image_large = {'query': 'random', 'description': 'unrelated', 'alt': 'other', 'width': 1200}

        score_small = score_image_relevance(image_small, ['tech'], ['innovation'])
        score_large = score_image_relevance(image_large, ['tech'], ['innovation'])

        assert score_small == 0.0
        assert score_large == 0.5  # Only size bonus

    def test_combined_scoring(self):
        """Should combine headline, category, and size scoring."""
        image = {
            'query': 'technology innovation startup',
            'description': 'digital business',
            'alt': 'modern tech',
            'width': 1500
        }

        score = score_image_relevance(
            image,
            headline_keywords=['technology', 'startup'],  # 2 matches × 2 = 4
            category_keywords=['business', 'digital', 'innovation']  # 3 matches × 1 = 3
        )

        # Headline: 4 + Category: 3 + Size bonus: 0.5 = 7.5
        assert score == 7.5


class TestTopicSourceMatching:
    """Tests for source-to-topic matching."""

    def test_exact_match(self):
        """Should match exact source names."""
        assert matches_topic_source('hackernews', ['hackernews', 'lobsters'])
        assert matches_topic_source('lobsters', ['hackernews', 'lobsters'])

    def test_prefix_match(self):
        """Should match source prefixes ending with underscore."""
        assert matches_topic_source('tech_verge', ['tech_', 'news_'])
        assert matches_topic_source('tech_wired', ['tech_', 'news_'])
        assert matches_topic_source('news_bbc', ['tech_', 'news_'])

    def test_no_match(self):
        """Should return False when no prefix matches."""
        assert not matches_topic_source('reddit', ['tech_', 'news_'])
        assert not matches_topic_source('other_source', ['hackernews', 'lobsters'])

    def test_exact_vs_prefix_distinction(self):
        """Should distinguish between exact and prefix matching."""
        # 'tech' should NOT match 'tech_' prefix
        assert not matches_topic_source('tech', ['tech_'])

        # 'tech_verge' should NOT match exact 'tech'
        assert not matches_topic_source('tech_verge', ['tech'])

        # But 'tech' should match exact 'tech'
        assert matches_topic_source('tech', ['tech'])


class TestTrendFiltering:
    """Tests for filtering trends by topic."""

    def test_filters_trends_correctly(self):
        """Should filter trends matching topic sources."""
        trends = [
            {'title': 'HN Story', 'source': 'hackernews'},
            {'title': 'Lobsters Story', 'source': 'lobsters'},
            {'title': 'Reddit Story', 'source': 'reddit'},
            {'title': 'Tech Story', 'source': 'tech_verge'},
        ]

        tech_trends = filter_trends_by_topic(trends, ['hackernews', 'lobsters', 'tech_'])

        assert len(tech_trends) == 3
        assert any(t['source'] == 'hackernews' for t in tech_trends)
        assert any(t['source'] == 'lobsters' for t in tech_trends)
        assert any(t['source'] == 'tech_verge' for t in tech_trends)
        assert not any(t['source'] == 'reddit' for t in tech_trends)

    def test_empty_trends_list(self):
        """Should handle empty trends list."""
        filtered = filter_trends_by_topic([], ['hackernews'])
        assert filtered == []

    def test_no_matching_sources(self):
        """Should return empty list when no sources match."""
        trends = [
            {'title': 'Story 1', 'source': 'reddit'},
            {'title': 'Story 2', 'source': 'twitter'},
        ]

        filtered = filter_trends_by_topic(trends, ['hackernews', 'tech_'])
        assert filtered == []


class TestHeroImageSelection:
    """Tests for hero image selection logic."""

    def test_find_best_matching_image(self):
        """Should find image with best keyword match."""
        images = [
            {'id': '1', 'query': 'random nature', 'description': '', 'alt': '', 'width': 1000},
            {'id': '2', 'query': 'technology innovation', 'description': 'modern tech', 'alt': '', 'width': 1000},
            {'id': '3', 'query': 'business', 'description': '', 'alt': '', 'width': 1000},
        ]

        used_ids = set()
        hero = find_topic_hero_image(
            images,
            headline='New technology innovation breakthrough',
            category_keywords=['tech', 'digital'],
            fallback_index=0,
            used_image_ids=used_ids
        )

        assert hero['id'] == '2'  # Best match
        assert '2' in used_ids

    def test_uses_fallback_when_no_match(self):
        """Should use fallback index when no keywords match."""
        images = [
            {'id': '1', 'query': 'random', 'description': '', 'alt': '', 'width': 1000},
            {'id': '2', 'query': 'unrelated', 'description': '', 'alt': '', 'width': 1000},
        ]

        used_ids = set()
        hero = find_topic_hero_image(
            images,
            headline='Completely different topic',
            category_keywords=['other', 'keywords'],
            fallback_index=1,
            used_image_ids=used_ids
        )

        assert hero['id'] == '2'  # Fallback index 1
        assert '2' in used_ids

    def test_avoids_used_images(self):
        """Should avoid images that are already used."""
        images = [
            {'id': '1', 'query': 'tech', 'description': '', 'alt': '', 'width': 1000},
            {'id': '2', 'query': 'tech', 'description': '', 'alt': '', 'width': 1000},
        ]

        used_ids = {'1'}  # Image 1 already used
        hero = find_topic_hero_image(
            images,
            headline='tech news',
            category_keywords=[],
            fallback_index=0,
            used_image_ids=used_ids
        )

        assert hero['id'] == '2'  # Should pick image 2

    def test_handles_empty_images_list(self):
        """Should return empty dict when no images available."""
        hero = find_topic_hero_image(
            images=[],
            headline='Some headline',
            category_keywords=['tech'],
            fallback_index=0,
            used_image_ids=set()
        )

        assert hero == {}


class TestTopicPageGeneration:
    """Tests for topic page generation decisions."""

    def test_should_generate_with_enough_stories(self):
        """Should generate page when enough stories exist."""
        trends = [{'title': f'Story {i}'} for i in range(5)]
        assert should_generate_topic_page(trends, min_stories=3)

    def test_should_not_generate_with_few_stories(self):
        """Should not generate page with insufficient stories."""
        trends = [{'title': 'Story 1'}, {'title': 'Story 2'}]
        assert not should_generate_topic_page(trends, min_stories=3)

    def test_edge_case_exactly_minimum(self):
        """Should generate when exactly at minimum threshold."""
        trends = [{'title': f'Story {i}'} for i in range(3)]
        assert should_generate_topic_page(trends, min_stories=3)


class TestArticleImagePriority:
    """Tests for prioritizing article images over stock photos."""

    def test_uses_article_image_when_available(self):
        """Should use article image from RSS feed when available."""
        top_story = {
            'title': 'Breaking Tech News',
            'image_url': 'https://example.com/article-image.jpg'
        }

        hero = get_topic_hero_image_from_story_or_search(
            top_story,
            images=[],
            topic_keywords=[],
            fallback_index=0,
            used_image_ids=set()
        )

        assert hero['url_large'] == 'https://example.com/article-image.jpg'
        assert hero['source'] == 'article'
        assert hero['alt'] == 'Breaking Tech News'

    def test_falls_back_to_stock_photos(self):
        """Should fall back to stock photos when no article image."""
        top_story = {'title': 'Tech Story', 'image_url': None}
        images = [
            {'id': '1', 'query': 'technology', 'description': '', 'alt': '', 'width': 1000}
        ]

        used_ids = set()
        hero = get_topic_hero_image_from_story_or_search(
            top_story,
            images=images,
            topic_keywords=['tech', 'innovation'],
            fallback_index=0,
            used_image_ids=used_ids
        )

        assert hero['id'] == '1'
        assert '1' in used_ids
