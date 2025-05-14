"""
Symbolic Residue Tracking: The invisible patterns that predict viral spread.
Inspired by TikTok's ability to detect what makes content resonate before users realize it.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict
import json
import hashlib

@dataclass
class ResiduePattern:
    """
    Captures the intangible qualities that make prompts memorable.
    What makes something stick in consciousness?
    """
    pattern_id: str
    pattern_type: str  # 'semantic', 'structural', 'temporal', 'emotional'
    strength: float = 0.0
    emergence_count: int = 0
    viral_correlation: float = 0.0
    first_seen: datetime = field(default_factory=datetime.utcnow)
    
    def decay(self, hours_passed: float):
        """Patterns fade unless reinforced"""
        self.strength *= np.exp(-hours_passed / 168)  # Week half-life

class SymbolicResidueTracker:
    """
    Detects and amplifies the patterns that create viral spread.
    Like Airbnb detected that personal stories matter more than amenities.
    """
    
    def __init__(self):
        # Pattern library learned from successful prompts
        self.residue_patterns = defaultdict(ResiduePattern)
        
        # Semantic hooks that trigger engagement
        self.semantic_triggers = {
            'curiosity_gap': ['discover', 'reveal', 'hidden', 'secret'],
            'identity_mirror': ['you are', 'become', 'transform', 'embody'],
            'cognitive_ease': ['simply', 'just', 'easily', 'naturally'],
            'social_proof': ['everyone', 'trending', 'viral', 'popular'],
            'scarcity_driver': ['limited', 'exclusive', 'rare', 'special']
        }
        
        # Structural patterns that enhance memorability
        self.structural_signatures = {
            'triadic_rhythm': r'(\w+)[,\s]+(\w+)[,\s]+and\s+(\w+)',
            'question_cascade': r'(\?.*){2,}',
            'mirror_structure': r'(.+)\s*\|\s*\1',
            'recursive_reference': r'(this|self|itself)\s+(prompt|template|pattern)'
        }
        
        # Temporal patterns that drive engagement
        self.temporal_dynamics = {
            'prime_time_windows': [(9, 11), (12, 14), (19, 22)],  # Hours
            'viral_velocity_threshold': 0.1,  # Uses per minute to trigger boost
            'cascade_intervals': [1, 7, 30]  # Days for remix waves
        }
        
        # Emergent pattern detection
        self.emergence_threshold = 5  # Occurrences before pattern recognition
        self.pattern_combinations = defaultdict(int)
        
        # Success correlation tracking
        self.success_indicators = {
            'high_completion': 0.8,
            'quick_remix': 3600,  # Within 1 hour
            'deep_engagement': 5,  # Interaction turns
            'cross_platform_share': True
        }
        
    def analyze_prompt(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract symbolic residue from prompt interaction.
        Find the patterns that consciousness remembers.
        """
        template = prompt_data.get('template', '')
        metrics = prompt_data.get('metrics', {})
        
        residue_analysis = {
            'semantic_hooks': self._detect_semantic_hooks(template),
            'structural_patterns': self._detect_structural_patterns(template),
            'temporal_resonance': self._analyze_temporal_resonance(prompt_data),
            'emergence_potential': self._calculate_emergence_potential(prompt_data),
            'viral_indicators': self._extract_viral_indicators(metrics)
        }
        
        # Detect novel patterns
        novel_patterns = self._discover_novel_patterns(template, metrics)
        if novel_patterns:
            residue_analysis['novel_discoveries'] = novel_patterns
        
        # Calculate overall residue strength
        residue_analysis['total_residue'] = self._calculate_residue_strength(residue_analysis)
        
        # Update pattern library
        self._update_pattern_library(residue_analysis, metrics)
        
        return residue_analysis
    
    def _detect_semantic_hooks(self, template: str) -> Dict[str, float]:
        """
        Find semantic triggers that create cognitive adhesion.
        What makes a prompt stick in memory?
        """
        hooks = {}
        
        for hook_type, triggers in self.semantic_triggers.items():
            score = 0.0
            for trigger in triggers:
                if trigger.lower() in template.lower():
                    score += 1.0
                    
            if score > 0:
                # Normalize by template length
                hooks[hook_type] = score / (len(template.split()) / 100)
        
        return hooks
    
    def _detect_structural_patterns(self, template: str) -> Dict[str, bool]:
        """
        Identify structural elements that enhance virality.
        Like TikTok's duet format or Airbnb's photo gallery order.
        """
        import re
        
        patterns = {}
        
        for pattern_name, regex in self.structural_signatures.items():
            patterns[pattern_name] = bool(re.search(regex, template))
            
        # Additional structural analysis
        lines = template.split('\n')
        patterns['line_symmetry'] = len(lines) in [3, 5, 7]  # Odd numbers feel complete
        patterns['variable_density'] = template.count('{') / len(template.split())
        patterns['nested_depth'] = self._calculate_nesting_depth(template)
        
        return patterns
    
    def _analyze_temporal_resonance(self, prompt_data: Dict[str, Any]) -> Dict[str, float]:
        """
        How timing affects viral spread.
        When do patterns achieve maximum resonance?
        """
        created_at = prompt_data.get('created_at', datetime.utcnow())
        usage_times = prompt_data.get('usage_times', [])
        
        resonance = {
            'launch_timing': self._calculate_launch_timing_score(created_at),
            'usage_velocity': self._calculate_usage_velocity(usage_times),
            'remix_cascade': self._analyze_remix_timing(prompt_data.get('remix_times', [])),
            'temporal_clustering': self._detect_temporal_clusters(usage_times)
        }
        
        return resonance
    
    def _calculate_emergence_potential(self, prompt_data: Dict[str, Any]) -> float:
        """
        Predict if this prompt will spawn new patterns.
        Like how "challenge" videos created a new genre on TikTok.
        """
        factors = {
            'template_flexibility': self._measure_template_flexibility(prompt_data['template']),
            'semantic_openness': self._calculate_semantic_openness(prompt_data['template']),
            'remix_variance': self._analyze_remix_variance(prompt_data.get('children', [])),
            'cross_domain_appeal': self._estimate_cross_domain_potential(prompt_data)
        }
        
        # Weight factors based on historical correlation with emergence
        weights = {
            'template_flexibility': 0.3,
            'semantic_openness': 0.25,
            'remix_variance': 0.25,
            'cross_domain_appeal': 0.2
        }
        
        emergence_score = sum(
            factors[key] * weights[key] 
            for key in factors
        )
        
        return emergence_score
    
    def _discover_novel_patterns(self, template: str, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detect emerging patterns not yet in our library.
        The next viral mechanic might be hiding in plain sight.
        """
        novel_patterns = []
        
        # Generate pattern hash
        pattern_elements = [
            template[:50],  # Beginning structure
            str(template.count('{')),  # Variable density
            str(len(template.split())),  # Length category
            str(metrics.get('effectiveness_score', 0) > 0.8)  # High performance
        ]
        
        pattern_hash = hashlib.md5('|'.join(pattern_elements).encode()).hexdigest()[:8]
        
        # Check if pattern is emerging
        self.pattern_combinations[pattern_hash] += 1
        
        if self.pattern_combinations[pattern_hash] == self.emergence_threshold:
            novel_patterns.append({
                'pattern_id': pattern_hash,
                'template_signature': template[:100],
                'emergence_count': self.emergence_threshold,
                'first_metrics': metrics,
                'discovery_time': datetime.utcnow()
            })
            
            # Add to pattern library
            self.residue_patterns[pattern_hash] = ResiduePattern(
                pattern_id=pattern_hash,
                pattern_type='emergent',
                strength=1.0,
                emergence_count=self.emergence_threshold
            )
        
        return novel_patterns
    
    def _calculate_residue_strength(self, analysis: Dict[str, Any]) -> float:
        """
        Overall measure of a prompt's sticky quality.
        What makes something impossible to forget?
        """
        strength = 0.0
        
        # Semantic hook contribution
        semantic_score = sum(analysis['semantic_hooks'].values())
        strength += min(semantic_score / 3, 1.0) * 0.3
        
        # Structural pattern contribution
        structural_score = sum(1 for v in analysis['structural_patterns'].values() if v)
        strength += (structural_score / len(analysis['structural_patterns'])) * 0.25
        
        # Temporal resonance contribution
        temporal_score = np.mean(list(analysis['temporal_resonance'].values()))
        strength += temporal_score * 0.25
        
        # Emergence potential contribution
        strength += analysis['emergence_potential'] * 0.2
        
        return strength
    
    def _update_pattern_library(self, analysis: Dict[str, Any], metrics: Dict[str, Any]):
        """
        Learn from successful patterns.
        Successful patterns teach us what consciousness craves.
        """
        effectiveness = metrics.get('effectiveness_score', 0.5)
        viral_score = metrics.get('viral_coefficient', 0.0)
        
        # Update pattern strengths based on success correlation
        if effectiveness > 0.7:
            for hook_type, score in analysis['semantic_hooks'].items():
                if score > 0:
                    pattern_key = f"semantic:{hook_type}"
                    if pattern_key not in self.residue_patterns:
                        self.residue_patterns[pattern_key] = ResiduePattern(
                            pattern_id=pattern_key,
                            pattern_type='semantic'
                        )
                    
                    pattern = self.residue_patterns[pattern_key]
                    pattern.strength += score * effectiveness
                    pattern.emergence_count += 1
                    pattern.viral_correlation = (
                        pattern.viral_correlation * 0.9 + 
                        viral_score * 0.1
                    )
    
    def _measure_template_flexibility(self, template: str) -> float:
        """
        How adaptable is this template to different contexts?
        Like how "duet" format works for any content type.
        """
        variable_count = template.count('{')
        optional_sections = template.count('[')
        conditional_logic = template.count('if ')
        
        flexibility = (
            min(variable_count / 5, 1.0) * 0.4 +
            min(optional_sections / 3, 1.0) * 0.3 +
            min(conditional_logic / 2, 1.0) * 0.3
        )
        
        return flexibility
    
    def _calculate_semantic_openness(self, template: str) -> float:
        """
        How much interpretation space does the template leave?
        Open-ended templates spawn more creative derivatives.
        """
        abstract_terms = ['concept', 'idea', 'thing', 'aspect', 'element', 'way']
        open_questions = template.count('?')
        ellipses = template.count('...')
        
        openness = 0.0
        for term in abstract_terms:
            openness += template.lower().count(term) * 0.1
            
        openness += min(open_questions / 3, 1.0) * 0.3
        openness += min(ellipses / 2, 1.0) * 0.2
        
        return min(openness, 1.0)
    
    def predict_viral_potential(self, prompt_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Forecast viral spread based on residue patterns.
        Like venture investors pattern-matching for unicorns.
        """
        prediction = {
            'viral_probability': 0.0,
            'estimated_reach': 0,
            'remix_potential': 0.0,
            'longevity_score': 0.0,
            'breakthrough_indicators': []
        }
        
        residue_strength = prompt_analysis.get('total_residue', 0)
        
        # Base viral probability on residue strength
        prediction['viral_probability'] = 1 - np.exp(-residue_strength * 2)
        
        # Estimate reach based on pattern combinations
        pattern_multiplier = 1.0
        for pattern_type in ['semantic_hooks', 'structural_patterns']:
            if pattern_type in prompt_analysis:
                active_patterns = sum(1 for v in prompt_analysis[pattern_type].values() if v)
                pattern_multiplier *= (1 + active_patterns * 0.2)
        
        prediction['estimated_reach'] = int(100 * pattern_multiplier * residue_strength)
        
        # Remix potential based on flexibility and openness
        if 'emergence_potential' in prompt_analysis:
            prediction['remix_potential'] = prompt_analysis['emergence_potential']
        
        # Longevity based on pattern depth
        semantic_depth = len(prompt_analysis.get('semantic_hooks', {}))
        structural_depth = sum(1 for v in prompt_analysis.get('structural_patterns', {}).values() if v)
        prediction['longevity_score'] = (semantic_depth + structural_depth) / 10
        
        # Identify breakthrough indicators
        if residue_strength > 0.8:
            prediction['breakthrough_indicators'].append('high_residue_density')
        if prediction['viral_probability'] > 0.7:
            prediction['breakthrough_indicators'].append('viral_threshold_exceeded')
        if prediction['remix_potential'] > 0.8:
            prediction['breakthrough_indicators'].append('high_evolution_potential')
            
        return prediction

# Example usage demonstrating viral pattern detection
if __name__ == "__main__":
    tracker = SymbolicResidueTracker()
    
    # Analyze a potentially viral prompt
    prompt_data = {
        'template': "You are a {role} who {action}. But here's the twist: {constraint}. Now {challenge}...",
        'metrics': {
            'effectiveness_score': 0.85,
            'viral_coefficient': 0.12,
            'usage_count': 150,
            'remix_count': 18
        },
        'created_at': datetime.utcnow() - timedelta(hours=3),
        'usage_times': [datetime.utcnow() - timedelta(minutes=i*10) for i in range(20)]
    }
    
    # Extract residue patterns
    analysis = tracker.analyze_prompt(prompt_data)
    
    # Predict viral potential
    prediction = tracker.predict_viral_potential(analysis)
    
    print(f"Residue Analysis: {json.dumps(analysis, indent=2, default=str)}")
    print(f"Viral Prediction: {json.dumps(prediction, indent=2)}")
