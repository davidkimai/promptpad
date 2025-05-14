"""
The Feed Algorithm: Where discovery happens.
Like TikTok's FYP but for cognitive patterns.
"""

import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import random

class FeedAlgorithm:
    """
    Sophisticated recommendation engine that learns what works.
    Surfaces quality over popularity, potential over past performance.
    """
    
    def __init__(self):
        self.recommendation_weights = {
            'effectiveness': 0.3,      # How well does it work?
            'novelty': 0.2,           # Is it different?
            'viral_potential': 0.2,    # Will it spread?
            'user_affinity': 0.15,    # Does it match user interests?
            'recency': 0.1,           # Is it fresh?
            'creator_trust': 0.05     # Is creator reliable?
        }
        
        # User behavior tracking
        self.user_interactions = defaultdict(lambda: {
            'views': [],
            'uses': [],
            'remixes': [],
            'skips': [],
            'categories': defaultdict(float)
        })
        
        # Global trend detection
        self.trending_patterns = defaultdict(float)
        self.emerging_creators = set()
        self.viral_thresholds = {
            'remix_rate': 0.1,    # 10% of users remix
            'share_rate': 0.05,   # 5% share externally
            'completion_rate': 0.8 # 80% complete interaction
        }
        
    def get_feed(self, user_id: str, count: int = 20) -> List[Dict[str, Any]]:
        """
        Generate personalized feed for user.
        Balances exploration with exploitation.
        """
        # Get user profile
        user_profile = self._build_user_profile(user_id)
        
        # Get candidate prompts
        candidates = self._gather_candidates(user_id, count * 5)
        
        # Score and rank
        scored_candidates = []
        for prompt in candidates:
            score = self._calculate_prompt_score(prompt, user_profile)
            scored_candidates.append((score, prompt))
        
        # Sort by score
        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        
        # Apply diversity filter
        diverse_feed = self._apply_diversity_filter(scored_candidates, count)
        
        # Mix in exploration
        final_feed = self._inject_exploration(diverse_feed, count)
        
        # Track impressions
        self._track_impressions(user_id, final_feed)
        
        return final_feed
    
    def record_interaction(self, user_id: str, prompt_id: str, 
                          interaction_type: str, metadata: Dict[str, Any]):
        """
        Track user interactions to improve recommendations.
        Every action teaches the algorithm.
        """
        timestamp = datetime.utcnow()
        
        interaction = {
            'prompt_id': prompt_id,
            'timestamp': timestamp,
            'type': interaction_type,
            'metadata': metadata
        }
        
        # Update user profile
        user_data = self.user_interactions[user_id]
        
        if interaction_type == 'view':
            user_data['views'].append(interaction)
        elif interaction_type == 'use':
            user_data['uses'].append(interaction)
            self._update_category_affinities(user_id, prompt_id, weight=1.0)
        elif interaction_type == 'remix':
            user_data['remixes'].append(interaction)
            self._update_category_affinities(user_id, prompt_id, weight=2.0)
        elif interaction_type == 'skip':
            user_data['skips'].append(interaction)
            self._update_category_affinities(user_id, prompt_id, weight=-0.5)
        
        # Update global patterns
        self._update_trending_patterns(prompt_id, interaction_type)
        
        # Detect viral moments
        self._check_viral_threshold(prompt_id)
    
    def _build_user_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Build comprehensive user profile from interaction history.
        Understands preferences without being creepy.
        """
        user_data = self.user_interactions[user_id]
        
        profile = {
            'user_id': user_id,
            'category_preferences': user_data['categories'],
            'interaction_patterns': self._analyze_interaction_patterns(user_data),
            'skill_level': self._estimate_skill_level(user_data),
            'exploration_appetite': self._calculate_exploration_appetite(user_data),
            'time_patterns': self._analyze_time_patterns(user_data)
        }
        
        return profile
    
    def _calculate_prompt_score(self, prompt: Dict[str, Any], 
                               user_profile: Dict[str, Any]) -> float:
        """
        Score prompt for specific user.
        Balances multiple optimization objectives.
        """
        scores = {}
        
        # Effectiveness score
        scores['effectiveness'] = prompt.get('effectiveness_score', 0.5)
        
        # Novelty score
        seen_similar = self._count_similar_seen(prompt, user_profile)
        scores['novelty'] = 1.0 / (1.0 + seen_similar)
        
        # Viral potential
        scores['viral_potential'] = self._calculate_viral_potential(prompt)
        
        # User affinity
        scores['user_affinity'] = self._calculate_user_affinity(prompt, user_profile)
        
        # Recency
        age_hours = (datetime.utcnow() - prompt['created_at']).total_seconds() / 3600
        scores['recency'] = np.exp(-age_hours / 168)  # Decay over week
        
        # Creator trust
        scores['creator_trust'] = self._get_creator_trust_score(prompt['creator_id'])
        
        # Weighted combination
        final_score = 0.0
        for factor, weight in self.recommendation_weights.items():
            final_score += weight * scores.get(factor, 0.0)
            
        # Boost for exploration
        if user_profile['exploration_appetite'] > 0.7:
            final_score *= 1.2
            
        return final_score
    
    def _calculate_viral_potential(self, prompt: Dict[str, Any]) -> float:
        """
        Predict viral spread before it happens.
        Key insight: Low friction + high value = viral.
        """
        # Current metrics
        usage_count = prompt.get('usage_count', 0)
        remix_count = prompt.get('remix_count', 0)
        unique_users = prompt.get('unique_users', 0)
        
        # Viral indicators
        remix_rate = remix_count / max(usage_count, 1)
        user_retention = unique_users / max(usage_count, 1)
        trending_momentum = prompt.get('trending_score', 0)
        
        # Time factor (newer prompts get boost)
        age_hours = (datetime.utcnow() - prompt['created_at']).total_seconds() / 3600
        recency_boost = 1.0 if age_hours < 24 else 0.8
        
        # Calculate potential
        viral_score = (
            0.4 * min(remix_rate * 10, 1.0) +      # Remix signal
            0.3 * user_retention +                  # Stickiness
            0.2 * trending_momentum +               # Current momentum
            0.1 * recency_boost                     # Fresh content bonus
        )
        
        return viral_score
    
    def _apply_diversity_filter(self, scored_candidates: List[tuple], 
                               target_count: int) -> List[Dict[str, Any]]:
        """
        Ensure feed has variety.
        Prevents echo chambers, encourages discovery.
        """
        selected = []
        seen_creators = set()
        seen_categories = defaultdict(int)
        max_per_creator = 2
        max_per_category = 5
        
        for score, prompt in scored_candidates:
            # Skip if too many from same creator
            if seen_creators.count(prompt['creator_id']) >= max_per_creator:
                continue
                
            # Skip if category is oversaturated
            category = self._get_prompt_category(prompt)
            if seen_categories[category] >= max_per_category:
                continue
                
            selected.append(prompt)
            seen_creators.add(prompt['creator_id'])
            seen_categories[category] += 1
            
            if len(selected) >= target_count:
                break
                
        return selected
    
    def _inject_exploration(self, feed: List[Dict[str, Any]], 
                           target_count: int) -> List[Dict[str, Any]]:
        """
        Mix in discovery content.
        10% random high-quality prompts for serendipity.
        """
        exploration_slots = max(2, int(target_count * 0.1))
        
        # Get random high-quality prompts
        exploration_prompts = self._get_exploration_candidates(exploration_slots)
        
        # Insert at random positions
        for prompt in exploration_prompts:
            if len(feed) >= target_count:
                index = random.randint(0, target_count - 1)
                feed[index] = prompt
            else:
                feed.append(prompt)
                
        return feed[:target_count]
    
    def _update_trending_patterns(self, prompt_id: str, interaction_type: str):
        """
        Track global patterns to identify trends early.
        What's about to go viral?
        """
        weight_map = {
            'view': 0.1,
            'use': 0.5,
            'remix': 2.0,
            'share': 1.5,
            'skip': -0.3
        }
        
        weight = weight_map.get(interaction_type, 0)
        self.trending_patterns[prompt_id] += weight
        
        # Decay old patterns
        for pid in list(self.trending_patterns.keys()):
            self.trending_patterns[pid] *= 0.99
            if self.trending_patterns[pid] < 0.01:
                del self.trending_patterns[pid]
    
    def _check_viral_threshold(self, prompt_id: str):
        """
        Detect when prompt crosses viral threshold.
        Trigger special handling for viral content.
        """
        prompt = self._get_prompt_data(prompt_id)
        
        if not prompt:
            return
            
        usage_count = prompt.get('usage_count', 0)
        remix_count = prompt.get('remix_count', 0)
        
        if usage_count > 0:
            remix_rate = remix_count / usage_count
            
            if remix_rate > self.viral_thresholds['remix_rate']:
                self._handle_viral_prompt(prompt_id)
    
    def _handle_viral_prompt(self, prompt_id: str):
        """
        Special handling for viral content.
        Boost exposure while maintaining quality.
        """
        # This would trigger notifications, special placement, etc.
        # Simplified for architecture demonstration
        self.trending_patterns[prompt_id] *= 2.0
        
    def _get_prompt_category(self, prompt: Dict[str, Any]) -> str:
        """
        Categorize prompt for diversity filtering.
        Uses NLP in production, simplified here.
        """
        template = prompt.get('template', '').lower()
        
        if 'startup' in template or 'business' in template:
            return 'business'
        elif 'code' in template or 'programming' in template:
            return 'technical'
        elif 'write' in template or 'story' in template:
            return 'creative'
        elif 'analyze' in template or 'data' in template:
            return 'analytical'
        else:
            return 'general'
    
    def _get_exploration_candidates(self, count: int) -> List[Dict[str, Any]]:
        """
        Get high-quality random prompts for exploration.
        Ensures users discover outside their bubble.
        """
        # This would query database for random high-performing prompts
        # Simplified for demonstration
        return []
    
    def _get_prompt_data(self, prompt_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve prompt data by ID.
        Would query database in production.
        """
        # Simplified for demonstration
        return None

# Usage example showing viral mechanics
if __name__ == "__main__":
    algorithm = FeedAlgorithm()
    
    # User interacts with prompts
    algorithm.record_interaction(
        user_id="user_123",
        prompt_id="prompt_456",
        interaction_type="use",
        metadata={'satisfaction': 0.9}
    )
    
    # User creates a remix
    algorithm.record_interaction(
        user_id="user_123",
        prompt_id="prompt_456",
        interaction_type="remix",
        metadata={'modifications': 'minor'}
    )
    
    # Get personalized feed
    feed = algorithm.get_feed("user_123", count=20)
    
    # Track what goes viral
    print(f"Trending prompts: {list(algorithm.trending_patterns.keys())[:5]}")
