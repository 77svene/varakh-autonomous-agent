"""
Core Agent Implementation
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class AgentState(Enum):
    """Operational states of the agent"""
    IDLE = "idle"
    THINKING = "thinking"
    ACTING = "acting"
    LEARNING = "learning"
    ERROR = "error"


@dataclass
class AgentConfig:
    """Configuration for the agent"""
    name: str = "VARAKH"
    max_thought_depth: int = 10
    action_timeout: float = 30.0
    learning_rate: float = 0.01
    memory_limit: int = 10000
    enable_self_modification: bool = False
    log_level: str = "INFO"


class Agent:
    """
    Base Autonomous Agent Class
    
    This agent implements a cognitive cycle:
    1. Perceive - gather information from environment
    2. Reason - process information and form intentions
    3. Act - execute actions based on intentions
    4. Learn - update internal models from outcomes
    """
    
    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or AgentConfig()
        self.state = AgentState.IDLE
        self.memory: List[Dict[str, Any]] = []
        self.intentions: List[Dict[str, Any]] = []
        self._setup_logging()
        self.logger.info(f"Agent {self.config.name} initialized")
    
    def _setup_logging(self):
        """Configure logging for the agent"""
        self.logger = logging.getLogger(self.config.name)
        self.logger.setLevel(getattr(logging, self.config.log_level))
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    async def perceive(self) -> Dict[str, Any]:
        """
        Gather information from the environment.
        To be implemented by subclasses.
        """
        self.logger.debug("Perception phase - no implementation")
        return {}
    
    async def reason(self, perceptions: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Process perceptions and form intentions.
        To be implemented by subclasses.
        """
        self.logger.debug("Reasoning phase - no implementation")
        return []
    
    async def act(self, intentions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Execute intentions and return results.
        To be implemented by subclasses.
        """
        self.logger.debug("Action phase - no implementation")
        return []
    
    async def learn(self, experiences: List[Dict[str, Any]]) -> None:
        """
        Update internal models based on experiences.
        To be implemented by subclasses.
        """
        self.logger.debug("Learning phase - no implementation")
    
    async def cognitive_cycle(self) -> None:
        """Execute one full cognitive cycle"""
        try:
            self.state = AgentState.THINKING
            perceptions = await self.perceive()
            
            self.state = AgentState.THINKING
            intentions = await self.reason(perceptions)
            
            self.state = AgentState.ACTING
            results = await self.act(intentions)
            
            self.state = AgentState.LEARNING
            experiences = [
                {"perceptions": perceptions,
                 "intentions": intentions,
                 "results": results}
            ]
            await self.learn(experiences)
            
            # Store in memory
            self.memory.append({
                "perceptions": perceptions,
                "intentions": intentions,
                "results": results
            })
            
            # Trim memory if needed
            if len(self.memory) > self.config.memory_limit:
                self.memory = self.memory[-self.config.memory_limit:]
            
            self.state = AgentState.IDLE
            
        except Exception as e:
            self.logger.error(f"Error in cognitive cycle: {e}", exc_info=True)
            self.state = AgentState.ERROR
            raise
    
    async def run(self, cycles: int = 0) -> None:
        """
        Run the agent for a specified number of cycles.
        If cycles=0, run indefinitely until stopped.
        """
        cycle_count = 0
        self.logger.info(f"Starting agent run for {cycles if cycles > 0 else 'indefinite'} cycles")
        
        try:
            while cycles == 0 or cycle_count < cycles:
                await self.cognitive_cycle()
                cycle_count += 1
                
                if cycle_count % 10 == 0:
                    self.logger.info(f"Completed {cycle_count} cognitive cycles")
                
                # Small delay to prevent overwhelming
                await asyncio.sleep(0.1)
                
        except KeyboardInterrupt:
            self.logger.info("Agent stopped by user")
        except Exception as e:
            self.logger.error(f"Agent terminated with error: {e}", exc_info=True)
            raise
        finally:
            self.logger.info(f"Agent stopped after {cycle_count} cycles")


if __name__ == "__main__":
    # Example usage
    async def main():
        agent = Agent()
        await agent.run(cycles=5)
    
    asyncio.run(main())
