"""
Recursive Memory Shell: Where prompts evolve through use.
Each interaction deepens the prompt's understanding of itself.
Like how Airbnb listings improve through guest feedback.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from collections import defaultdict
from datetime import datetime
import json
import uuid

@dataclass
class MemoryLayer:
    """
    Single layer of recursive memory.
    Each use adds depth, like tree rings.
    """
    layer_id: str
    depth: int
    created_at: datetime
    interaction_count: int = 0
    learned_patterns: Dict[str, float] = field(default_factory=dict)
    user_adaptations: Dict[str, Any] = field(default_factory=dict)
    effectiveness_delta: float = 0.0
    
    def integrate_experience(self, interaction_data: Dict[str, Any]):
        """Memory deepens through experience"""
        self.interaction_count += 1
        
        # Learn from user patterns
        user_id = interaction_data.get('user_id')
        if user_id:
            if user_id not in self.user_adaptations:
                self.user_adaptations[user_id] = defaultdict(float)
            
            # Track what works for each user
            success_metric = interaction_data.get('success_metric', 0.5)
            self.user_adaptations[user_id]['success_rate'] = (
                self.user_adaptations[user_id]['success_rate'] * 0.9 +
                success_metric * 0.1
            )
        
        # Update learned patterns
        patterns = interaction_data.get('patterns', {})
        for pattern, strength in patterns.items():
            if pattern not in self.learned_patterns:
                self.learned_patterns[pattern] = 0.0
            self.learned_patterns[pattern] = (
                self.learned_patterns[pattern] * 0.8 +
                strength * 0.2
            )

class RecursiveMemoryShell:
    """
    A memory architecture that deepens through use.
    Each prompt becomes wiser through collective interaction.
    Inspired by how TikTok algorithm learns from every swipe.
    """
    
    def __init__(self, prompt_id: str, initial_template: str):
        self.id = prompt_id
        self.initial_template = initial_template
        self.current_template = initial_template
        
        # Memory layers accumulate over time
        self.memory_layers: List[MemoryLayer] = []
        self.current_depth = 0
        
        # Behavioral patterns learned through use
        self.behavioral_memory = {
            'successful_contexts': defaultdict(float),
            'failure_patterns': defaultdict(float),
            'user_preferences': defaultdict(dict),
            'optimal_parameters': defaultdict(float),
            'remix_genealogy': []
        }
        
        # Recursive improvements
        self.evolution_history = []
        self.mutation_rate = 0.05  # Small changes over time
        
        # Performance tracking
        self.performance_metrics = {
            'total_uses': 0,
            'success_rate': 0.5,
            'adaptation_velocity': 0.0,
            'memory_density': 0.0
        }
        
        # Initialize first memory layer
        self._create_new_layer()
    
    def remember(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Core method: Learn from each interaction.
        Memory compounds like interest.
        """
        self.performance_metrics['total_uses'] += 1
        
        # Extract interaction metadata
        context = interaction.get('context', {})
        result = interaction.get('result', {})
        user_id = interaction.get('user_id')
        success_metric = result.get('success', 0.5)
        
        # Update current memory layer
        current_layer = self.memory_layers[-1]
        current_layer.integrate_experience({
            'user_id': user_id,
            'success_metric': success_metric,
            'patterns': self._extract_patterns(context, result)
        })
        
        # Learn behavioral patterns
        self._update_behavioral_memory(context, result, user_id)
        
        # Check if new layer needed (depth increase)
        if self._should_deepen_memory(current_layer):
            self._create_new_layer()
            self._evolve_template()
        
        # Calculate memory response
        memory_response = self._generate_memory_response(context, user_id)
        
        return {
            'adapted_template': self.current_template,
            'memory_depth': self.current_depth,
            'personalization': memory_response,
            'evolution_stage': len(self.evolution_history)
        }
    
    def _extract_patterns(self, context: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract meaningful patterns from interaction.
        What made this interaction successful or not?
        """
        patterns = {}
        
        # Context patterns
        for key, value in context.items():
            if isinstance(value, str):
                pattern_key = f"context_{key}_{value[:20]}"
                patterns[pattern_key] = result.get('success', 0.5)
        
        # Result patterns
        response_length = len(str(result.get('response', '')))
        patterns['response_length_category'] = self._categorize_length(response_length)
        
        # Timing patterns
        execution_time = result.get('execution_time', 1.0)
        patterns['speed_category'] = self._categorize_speed(execution_time)
        
        # Success correlation patterns
        if result.get('success', 0.5) > 0.8:
            patterns['high_success_indicator'] = 1.0
            
        return patterns
    
    def _update_behavioral_memory(self, context: Dict[str, Any], result: Dict[str, Any], user_id: str):
        """
        Build behavioral understanding over time.
        Like how Airbnb hosts learn guest preferences.
        """
        success = result.get('success', 0.5)
        
        # Track successful contexts
        context_key = self._generate_context_key(context)
        self.behavioral_memory['successful_contexts'][context_key] = (
            self.behavioral_memory['successful_contexts'][context_key] * 0.9 +
            success * 0.1
        )
        
        # Track failure patterns
        if success < 0.3:
            failure_key = f"{context_key}_failure"
            self.behavioral_memory['failure_patterns'][failure_key] += 1
        
        # User preference learning
        if user_id:
            if user_id not in self.behavioral_memory['user_preferences']:
                self.behavioral_memory['user_preferences'][user_id] = {}
            
            user_prefs = self.behavioral_memory['user_preferences'][user_id]
            user_prefs['avg_success'] = (
                user_prefs.get('avg_success', 0.5) * 0.9 +
                success * 0.1
            )
            user_prefs['preferred_style'] = self._infer_style_preference(context, result)
    
    def _should_deepen_memory(self, current_layer: MemoryLayer) -> bool:
        """
        Decide when to create new memory layer.
        Like annual rings in trees.
        """
        # Deepen after significant interactions
        if current_layer.interaction_count >= 100:
            return True
            
        # Deepen if effectiveness plateaus
        if abs(current_layer.effectiveness_delta) < 0.01 and current_layer.interaction_count > 20:
            return True
            
        # Deepen if patterns stabilize
        pattern_stability = self._calculate_pattern_stability(current_layer.learned_patterns)
        if pattern_stability > 0.9 and current_layer.interaction_count > 50:
            return True
            
        return False
    
    def _create_new_layer(self):
        """
        Add new memory layer, increasing depth.
        Each layer represents accumulated wisdom.
        """
        new_layer = MemoryLayer(
            layer_id=str(uuid.uuid4()),
            depth=self.current_depth,
            created_at=datetime.utcnow()
        )
        
        # Inherit patterns from previous layer
        if self.memory_layers:
            previous_layer = self.memory_layers[-1]
            new_layer.learned_patterns = previous_layer.learned_patterns.copy()
            new_layer.user_adaptations = previous_layer.user_adaptations.copy()
        
        self.memory_layers.append(new_layer)
        self.current_depth += 1
        
        # Update memory density metric
        self.performance_metrics['memory_density'] = self._calculate_memory_density()
    
    def _evolve_template(self):
        """
        Template evolves based on learned patterns.
        Like how genetic algorithms improve over generations.
        """
        # Analyze what's working
        successful_patterns = self._identify_successful_patterns()
        
        # Generate mutation
        mutation = self._generate_template_mutation(successful_patterns)
        
        if mutation:
            # Apply mutation
            old_template = self.current_template
            self.current_template = mutation
            
            # Record evolution
            self.evolution_history.append({
                'generation': len(self.evolution_history) + 1,
                'old_template': old_template,
                'new_template': mutation,
                'trigger_patterns': successful_patterns,
                'timestamp': datetime.utcnow()
            })
            
            # Adjust mutation rate based on success
            self._adjust_mutation_rate()
    
    def _generate_memory_response(self, context: Dict[str, Any], user_id: Optional[str]) -> Dict[str, Any]:
        """
        Generate response based on accumulated memory.
        Personalized for user if history exists.
        """
        response = {
            'confidence': self._calculate_confidence_score(),
            'adaptations': {},
            'suggestions': []
        }
        
        # Apply user-specific adaptations
        if user_id and user_id in self.behavioral_memory['user_preferences']:
            user_prefs = self.behavioral_memory['user_preferences'][user_id]
            response['adaptations']['style'] = user_prefs.get('preferred_style', 'default')
            response['adaptations']['success_prediction'] = user_prefs.get('avg_success', 0.5)
        
        # Apply context-specific adaptations
        context_key = self._generate_context_key(context)
        if context_key in self.behavioral_memory['successful_contexts']:
            success_rate = self.behavioral_memory['successful_contexts'][context_key]
            response['adaptations']['context_confidence'] = success_rate
        
        # Generate suggestions based on patterns
        top_patterns = self._get_top_patterns()
        for pattern, strength in top_patterns[:3]:
            response['suggestions'].append({
                'pattern': pattern,
                'strength': strength,
                'recommendation': self._pattern_to_recommendation(pattern)
            })
        
        return response
    
    def _calculate_memory_density(self) -> float:
        """
        Measure how much wisdom is packed into memory.
        Like information density in DNA.
        """
        if not self.memory_layers:
            return 0.0
            
        total_patterns = sum(
            len(layer.learned_patterns) 
            for layer in self.memory_layers
        )
        
        total_interactions = sum(
            layer.interaction_count 
            for layer in self.memory_layers
        )
        
        # Density increases with patterns per interaction
        density = total_patterns / max(total_interactions, 1)
        
        # Bonus for user adaptations
        total_users = len(self.behavioral_memory['user_preferences'])
        user_density = total_users / max(total_interactions, 1)
        
        return (density * 0.7 + user_density * 0.3)
    
    def _calculate_confidence_score(self) -> float:
        """
        How confident is the memory in its adaptations?
        Based on volume and consistency of experiences.
        """
        # Base confidence on experience volume
        experience_factor = min(self.performance_metrics['total_uses'] / 1000, 1.0)
        
        # Factor in success rate
        success_factor = self.performance_metrics['success_rate']
        
        # Factor in pattern stability
        pattern_stability = self._calculate_average_pattern_stability()
        
        # Factor in evolution success
        evolution_factor = self._calculate_evolution_success()
        
        confidence = (
            experience_factor * 0.3 +
            success_factor * 0.3 +
            pattern_stability * 0.2 +
            evolution_factor * 0.2
        )
        
        return confidence
    
    def _identify_successful_patterns(self) -> List[Tuple[str, float]]:
        """
        Find patterns that correlate with success.
        Success leaves clues in the data.
        """
        successful_patterns = []
        
        # Analyze all layers
        for layer in self.memory_layers:
            for pattern, strength in layer.learned_patterns.items():
                if strength > 0.7:  # High correlation with success
                    successful_patterns.append((pattern, strength))
        
        # Sort by strength
        successful_patterns.sort(key=lambda x: x[1], reverse=True)
        
        return successful_patterns[:10]  # Top 10 patterns
    
    def get_memory_state(self) -> Dict[str, Any]:
        """
        Export current memory state.
        For persistence or analysis.
        """
        return {
            'id': self.id,
            'current_template': self.current_template,
            'depth': self.current_depth,
            'layer_count': len(self.memory_layers),
            'total_interactions': self.performance_metrics['total_uses'],
            'success_rate': self.performance_metrics['success_rate'],
            'memory_density': self.performance_metrics['memory_density'],
            'evolution_count': len(self.evolution_history),
            'top_patterns': self._get_top_patterns()[:5],
            'user_count': len(self.behavioral_memory['user_preferences'])
        }

# Example demonstrating recursive memory evolution
if __name__ == "__main__":
    # Create a new recursive memory shell
    memory = RecursiveMemoryShell(
        prompt_id="prompt_001",
        initial_template="As a {role}, help me {task} by {approach}"
    )
    
    # Simulate interactions that teach the memory
    for i in range(150):
        interaction = {
            'context': {
                'role': ['consultant', 'advisor', 'expert'][i % 3],
                'task': ['analyze', 'improve', 'design'][i % 3],
                'approach': ['step-by-step', 'creatively', 'systematically'][i % 3]
            },
            'result': {
                'success': 0.7 + (i / 1000),  # Improving over time
                'execution_time': 2.0 - (i / 200),  # Getting faster
                'response': f"Generated response {i}"
            },
            'user_id': f"user_{i % 10}"  # 10 different users
        }
        
        memory_response = memory.remember(interaction)
        
        if i % 50 == 0:
            print(f"Interaction {i}:")
            print(f"  Memory depth: {memory_response['memory_depth']}")
            print(f"  Evolution stage: {memory_response['evolution_stage']}")
            print(f"  Current template: {memory.current_template}")
            print()
    
    # Display final memory state
    final_state = memory.get_memory_state()
    print(f"
