"""
PromptShell: The atomic unit of collective intelligence.
Each prompt is a living container that evolves through use, like TikTok sounds.
"""

import uuid
import time
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta

@dataclass
class ExecutionMetrics:
    """Track what makes prompts effective"""
    completion_time: float = 0.0
    user_satisfaction: float = 0.0
    objective_success: float = 0.0
    cognitive_load: float = 0.0
    interaction_depth: int = 0
    
    def calculate_effectiveness(self) -> float:
        """Weighted formula learned from successful prompts"""
        return (
            0.3 * self.user_satisfaction +
            0.25 * self.objective_success +
            0.2 * (1.0 - min(self.cognitive_load, 1.0)) +
            0.15 * min(self.interaction_depth / 5.0, 1.0) +
            0.1 * (1.0 - min(self.completion_time / 30.0, 1.0))
        )

class PromptShell:
    """
    Core prompt container that improves through collective use.
    Embeds viral mechanics without surface complexity.
    """
    
    def __init__(self, creator_id: str, template: str = "", parent_id: Optional[str] = None):
        self.id = str(uuid.uuid4())
        self.creator_id = creator_id
        self.template = template
        self.parent_id = parent_id
        self.children: List[str] = []
        
        # Usage tracking
        self.usage_count = 0
        self.unique_users = set()
        self.effectiveness_score = 0.5  # Start neutral
        
        # Temporal mechanics
        self.created_at = datetime.utcnow()
        self.last_used_at = None
        self.expiry_time = None  # For time-limited prompts
        
        # Evolution tracking
        self.version = 1
        self.mutations: List[Dict[str, Any]] = []
        self.execution_history: List[ExecutionMetrics] = []
        
        # Viral mechanics
        self.remix_count = 0
        self.share_count = 0
        self.trending_score = 0.0
        self.viral_coefficient = 0.0
        
        # Revenue tracking
        self.total_earned = 0.0
        self.royalty_rate = 0.7  # Creator gets 70%
        
    def execute(self, context: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Execute prompt with context, tracking all metrics.
        Each use makes the prompt smarter.
        """
        start_time = time.time()
        
        # Track unique users
        self.unique_users.add(user_id)
        self.usage_count += 1
        self.last_used_at = datetime.utcnow()
        
        # Execute against AI provider
        result = self._execute_prompt(context)
        
        # Calculate metrics
        execution_time = time.time() - start_time
        metrics = ExecutionMetrics(
            completion_time=execution_time,
            user_satisfaction=result.get('satisfaction', 0.5),
            objective_success=result.get('success', 0.5),
            cognitive_load=self._estimate_cognitive_load(result),
            interaction_depth=result.get('turns', 1)
        )
        
        # Update effectiveness
        self.execution_history.append(metrics)
        self._update_effectiveness_score(metrics)
        
        # Check for viral potential
        self._update_viral_metrics(metrics)
        
        return {
            'result': result,
            'metrics': metrics,
            'prompt_id': self.id,
            'effectiveness': self.effectiveness_score
        }
    
    def fork(self, new_creator_id: str, modifications: Dict[str, Any] = None) -> 'PromptShell':
        """
        Create a remix/fork of this prompt.
        Original creator gets royalties from derivatives.
        """
        child = PromptShell(
            creator_id=new_creator_id,
            template=self._apply_modifications(modifications),
            parent_id=self.id
        )
        
        # Track lineage
        self.children.append(child.id)
        self.remix_count += 1
        
        # Inherit some reputation
        child.effectiveness_score = self.effectiveness_score * 0.8
        
        # Update viral metrics
        self.viral_coefficient = self.remix_count / max(self.usage_count, 1)
        
        return child
    
    def lease(self, duration_hours: int, lessee_id: str) -> Dict[str, Any]:
        """
        Time-based leasing like Airbnb.
        Temporary exclusive access to high-performing prompts.
        """
        lease_price = self._calculate_lease_price(duration_hours)
        expiry = datetime.utcnow() + timedelta(hours=duration_hours)
        
        lease = {
            'prompt_id': self.id,
            'lessee_id': lessee_id,
            'start_time': datetime.utcnow(),
            'expiry_time': expiry,
            'price': lease_price,
            'creator_earnings': lease_price * self.royalty_rate
        }
        
        # Update prompt revenue
        self.total_earned += lease['creator_earnings']
        
        return lease
    
    def _execute_prompt(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actual prompt execution against AI provider.
        Adapts to different platforms automatically.
        """
        # This would integrate with AI providers
        # Simplified for architecture demonstration
        filled_template = self.template.format(**context)
        
        # Simulate execution
        return {
            'response': f"Executed: {filled_template}",
            'success': 0.8,
            'satisfaction': 0.9,
            'turns': 2
        }
    
    def _update_effectiveness_score(self, metrics: ExecutionMetrics):
        """
        Rolling average that weights recent executions higher.
        Prompts get better through use.
        """
        new_score = metrics.calculate_effectiveness()
        
        # Exponential moving average
        alpha = 0.1  # Learning rate
        self.effectiveness_score = (
            alpha * new_score + 
            (1 - alpha) * self.effectiveness_score
        )
    
    def _estimate_cognitive_load(self, result: Dict[str, Any]) -> float:
        """
        Estimate mental effort required for this prompt.
        Lower is better for viral spread.
        """
        # Simplified heuristic based on response complexity
        response_length = len(result.get('response', ''))
        complexity_indicators = ['however', 'although', 'considering', 'alternatively']
        complexity_count = sum(1 for ind in complexity_indicators if ind in result.get('response', ''))
        
        return min(
            (response_length / 1000) + (complexity_count * 0.1),
            1.0
        )
    
    def _update_viral_metrics(self, metrics: ExecutionMetrics):
        """
        Calculate viral potential based on usage patterns.
        High effectiveness + low cognitive load = viral.
        """
        if metrics.calculate_effectiveness() > 0.8:
            self.trending_score += 0.1
            
        if metrics.cognitive_load < 0.3:
            self.trending_score += 0.05
            
        # Decay trending score over time
        time_decay = (datetime.utcnow() - self.created_at).total_seconds() / 86400
        self.trending_score *= (0.95 ** time_decay)
    
    def _calculate_lease_price(self, duration_hours: int) -> float:
        """
        Dynamic pricing based on effectiveness and demand.
        Like Airbnb's smart pricing.
        """
        base_price = 1.0  # $1 per hour base
        
        # Effectiveness multiplier
        effectiveness_multiplier = self.effectiveness_score * 2
        
        # Demand multiplier
        demand_multiplier = min(self.usage_count / 100, 3.0)
        
        # Viral bonus
        viral_bonus = self.viral_coefficient * 2
        
        return base_price * duration_hours * effectiveness_multiplier * demand_multiplier * (1 + viral_bonus)
    
    def _apply_modifications(self, modifications: Dict[str, Any] = None) -> str:
        """
        Apply modifications to create a fork.
        Preserves what works, allows innovation.
        """
        if not modifications:
            return self.template
            
        modified_template = self.template
        
        for key, value in modifications.items():
            if key == 'append':
                modified_template += f"\n{value}"
            elif key == 'prepend':
                modified_template = f"{value}\n" + modified_template
            elif key == 'replace':
                for old, new in value.items():
                    modified_template = modified_template.replace(old, new)
                    
        return modified_template
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize for storage/transmission"""
        return {
            'id': self.id,
            'creator_id': self.creator_id,
            'template': self.template,
            'parent_id': self.parent_id,
            'children': self.children,
            'usage_count': self.usage_count,
            'unique_users': len(self.unique_users),
            'effectiveness_score': self.effectiveness_score,
            'created_at': self.created_at.isoformat(),
            'last_used_at': self.last_used_at.isoformat() if self.last_used_at else None,
            'version': self.version,
            'remix_count': self.remix_count,
            'viral_coefficient': self.viral_coefficient,
            'trending_score': self.trending_score,
            'total_earned': self.total_earned
        }

# Example usage pattern that demonstrates virality
if __name__ == "__main__":
    # Creator makes original prompt
    original = PromptShell(
        creator_id="creator_123",
        template="You are a {role} helping with {task}. Start by {approach}."
    )
    
    # User tries it
    result = original.execute(
        context={
            'role': 'startup mentor',
            'task': 'finding product-market fit',
            'approach': 'understanding the problem deeply'
        },
        user_id="user_456"
    )
    
    # User loves it, creates a remix
    remix = original.fork(
        new_creator_id="user_456",
        modifications={
            'append': "Focus especially on customer pain points."
        }
    )
    
    # Remix goes viral
    for i in range(100):
        remix.execute(
            context={
                'role': 'growth advisor',
                'task': 'scaling user acquisition',
                'approach': 'analyzing current metrics'
            },
            user_id=f"user_{i}"
        )
    
    # Original creator earns from derivative success
    print(f"Original effectiveness: {original.effectiveness_score}")
    print(f"Remix effectiveness: {remix.effectiveness_score}")
    print(f"Original viral coefficient: {original.viral_coefficient}")
    print(f"Creator earnings: ${original.total_earned}")
