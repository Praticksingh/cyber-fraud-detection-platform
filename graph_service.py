"""
Knowledge Graph Service for Fraud Detection
Supports Neo4j-style structure with in-memory fallback
"""

from datetime import datetime
from typing import List, Dict, Optional
import json


class FraudKnowledgeGraph:
    """
    Knowledge graph for tracking fraud patterns and relationships.
    Uses in-memory storage with optional Neo4j backend.
    """
    
    def __init__(self):
        """Initialize the knowledge graph with in-memory storage."""
        # In-memory storage
        self.nodes = {}  # {entity_value: node_data}
        self.edges = []  # [{source, target, relationship_type, weight}]
        
        # Try to import Neo4j (optional)
        self.neo4j_available = False
        try:
            from neo4j import GraphDatabase
            self.neo4j_available = True
            # Note: Connection would be initialized here if Neo4j is configured
        except ImportError:
            pass
    
    def add_entity(self, entity_type: str, value: str, risk_score: int):
        """
        Add or update an entity in the graph.
        
        Args:
            entity_type: Type of entity (phone, email, ip, pattern)
            value: Entity value (phone number, email address, etc.)
            risk_score: Risk score (0-100)
        """
        if value in self.nodes:
            # Update existing node
            node = self.nodes[value]
            node["risk_score"] = max(node["risk_score"], risk_score)
            node["incident_count"] += 1
            node["last_seen"] = datetime.now().isoformat()
        else:
            # Create new node
            self.nodes[value] = {
                "id": value,
                "entity_type": entity_type,
                "risk_score": risk_score,
                "incident_count": 1,
                "last_seen": datetime.now().isoformat(),
                "created_at": datetime.now().isoformat()
            }
    
    def add_relationship(self, source_value: str, target_value: str, relationship_type: str, weight: float = 1.0):
        """
        Add a relationship between two entities.
        
        Args:
            source_value: Source entity value
            target_value: Target entity value
            relationship_type: Type of relationship (similar_pattern, same_network, etc.)
            weight: Relationship strength (0-1)
        """
        # Check if relationship already exists
        for edge in self.edges:
            if (edge["source"] == source_value and 
                edge["target"] == target_value and 
                edge["relationship_type"] == relationship_type):
                # Update weight
                edge["weight"] = min(edge["weight"] + 0.1, 1.0)
                return
        
        # Add new relationship
        self.edges.append({
            "source": source_value,
            "target": target_value,
            "relationship_type": relationship_type,
            "weight": weight,
            "created_at": datetime.now().isoformat()
        })
    
    def get_connected_entities(self, entity_value: str, depth: int = 2) -> List[Dict]:
        """
        Get entities connected to the given entity up to specified depth.
        
        Args:
            entity_value: Starting entity value
            depth: Maximum traversal depth
            
        Returns:
            List of connected entities with their data
        """
        if entity_value not in self.nodes:
            return []
        
        visited = set()
        result = []
        
        def traverse(current_value, current_depth):
            if current_depth > depth or current_value in visited:
                return
            
            visited.add(current_value)
            
            if current_value in self.nodes:
                result.append(self.nodes[current_value])
            
            # Find connected nodes
            for edge in self.edges:
                if edge["source"] == current_value:
                    traverse(edge["target"], current_depth + 1)
                elif edge["target"] == current_value:
                    traverse(edge["source"], current_depth + 1)
        
        traverse(entity_value, 0)
        return result
    
    def propagate_risk(self, entity_value: str, decay_factor: float = 0.7) -> int:
        """
        Propagate risk score to connected entities.
        
        Args:
            entity_value: Starting entity value
            decay_factor: Risk decay factor for each hop (0-1)
            
        Returns:
            Number of entities affected
        """
        if entity_value not in self.nodes:
            return 0
        
        source_risk = self.nodes[entity_value]["risk_score"]
        affected = 0
        visited = set([entity_value])
        
        def propagate(current_value, current_risk, depth):
            nonlocal affected
            
            if depth > 2 or current_risk < 10:  # Stop if risk too low
                return
            
            # Find connected nodes
            for edge in self.edges:
                next_value = None
                if edge["source"] == current_value and edge["target"] not in visited:
                    next_value = edge["target"]
                elif edge["target"] == current_value and edge["source"] not in visited:
                    next_value = edge["source"]
                
                if next_value and next_value in self.nodes:
                    visited.add(next_value)
                    propagated_risk = int(current_risk * decay_factor * edge["weight"])
                    
                    # Update risk if higher
                    if propagated_risk > self.nodes[next_value]["risk_score"]:
                        self.nodes[next_value]["risk_score"] = propagated_risk
                        affected += 1
                    
                    # Continue propagation
                    propagate(next_value, propagated_risk, depth + 1)
        
        propagate(entity_value, source_risk, 0)
        return affected
    
    def get_graph_data_for_visualization(self, limit: int = 100) -> Dict:
        """
        Get graph data formatted for visualization.
        
        Args:
            limit: Maximum number of nodes to return
            
        Returns:
            Dictionary with nodes and edges for visualization
        """
        # Get top nodes by risk score
        sorted_nodes = sorted(
            self.nodes.values(),
            key=lambda x: x["risk_score"],
            reverse=True
        )[:limit]
        
        node_ids = {node["id"] for node in sorted_nodes}
        
        # Filter edges to only include nodes in the result
        filtered_edges = [
            edge for edge in self.edges
            if edge["source"] in node_ids and edge["target"] in node_ids
        ]
        
        # Format nodes for visualization
        vis_nodes = [
            {
                "id": node["id"],
                "label": node["id"][:15] + "..." if len(node["id"]) > 15 else node["id"],
                "risk_score": node["risk_score"],
                "entity_type": node["entity_type"],
                "incident_count": node["incident_count"]
            }
            for node in sorted_nodes
        ]
        
        # Format edges for visualization
        vis_edges = [
            {
                "source": edge["source"],
                "target": edge["target"],
                "relationship_type": edge["relationship_type"],
                "weight": edge["weight"]
            }
            for edge in filtered_edges
        ]
        
        return {
            "nodes": vis_nodes,
            "edges": vis_edges
        }
    
    def get_statistics(self) -> Dict:
        """Get graph statistics."""
        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "high_risk_nodes": sum(1 for n in self.nodes.values() if n["risk_score"] > 70),
            "medium_risk_nodes": sum(1 for n in self.nodes.values() if 30 < n["risk_score"] <= 70),
            "low_risk_nodes": sum(1 for n in self.nodes.values() if n["risk_score"] <= 30)
        }


# Global instance
fraud_graph = FraudKnowledgeGraph()
