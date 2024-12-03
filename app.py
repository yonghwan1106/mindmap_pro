import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px

def initialize_session_state():
    if 'learning_path' not in st.session_state:
        st.session_state.learning_path = []
    if 'study_logs' not in st.session_state:
        st.session_state.study_logs = []
    if 'concept_map' not in st.session_state:
        st.session_state.concept_map = nx.Graph()

def create_knowledge_map():
    G = nx.Graph()
    
    # Add nodes for different subjects and concepts
    concepts = {
        'Math': ['Calculus', 'Linear Algebra', 'Statistics'],
        'Physics': ['Mechanics', 'Thermodynamics', 'Waves'],
        'Chemistry': ['Organic', 'Inorganic', 'Physical']
    }
    
    for subject, topics in concepts.items():
        G.add_node(subject, type='subject')
        for topic in topics:
            G.add_node(topic, type='topic')
            G.add_edge(subject, topic)
    
    return G

def visualize_knowledge_map(G):
    pos = nx.spring_layout(G, k=1, iterations=50)
    
    edge_trace = go.Scatter(
        x=[], y=[], line=dict(width=0.5, color='#888'),
        hoverinfo='none', mode='lines')
    
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += (x0, x1, None)
        edge_trace['y'] += (y0, y1, None)
    
    node_trace = go.Scatter(
        x=[], y=[], text=[], mode='markers+text',
        hoverinfo='text', textposition='bottom center',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=30,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            )
        )
    )
    
    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'] += (x,)
        node_trace['y'] += (y,)
        node_trace['text'] += (node,)
    
    fig = go.Figure(data=[edge_trace, node_trace],
                   layout=go.Layout(
                       title='Knowledge Concept Map',
                       showlegend=False,
                       hovermode='closest',
                       margin=dict(b=20,l=5,r=5,t=40),
                       xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                   ))
    
    return fig

def create_study_dashboard():
    # Sample study data
    study_data = pd.DataFrame({
        'Date': pd.date_range(start='2024-01-01', periods=30, freq='D'),
        'Hours': np.random.uniform(2, 8, 30),
        'Subject': np.random.choice(['Math', 'Physics', 'Chemistry'], 30)
    })
    
    fig = px.line(study_data, x='Date', y='Hours', color='Subject',
                  title='Daily Study Hours by Subject')
    return fig

def main():
    st.set_page_config(page_title="MindMap Pro", layout="wide")
    initialize_session_state()
    
    st.title("MindMap Pro: Intelligent Learning Companion")
    
    tabs = st.tabs(["Knowledge Map", "Study Analytics", "Learning Path"])
    
    with tabs[0]:
        st.header("Interactive Knowledge Map")
        G = create_knowledge_map()
        fig = visualize_knowledge_map(G)
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("Add New Concept"):
            subject = st.selectbox("Select Subject", ['Math', 'Physics', 'Chemistry'])
            new_concept = st.text_input("Enter New Concept")
            if st.button("Add Concept"):
                if new_concept:
                    st.session_state.concept_map.add_node(new_concept)
                    st.session_state.concept_map.add_edge(subject, new_concept)
                    st.success(f"Added {new_concept} to {subject}")
    
    with tabs[1]:
        st.header("Study Analytics Dashboard")
        study_dashboard = create_study_dashboard()
        st.plotly_chart(study_dashboard, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Study Hours", "156.5", "+2.5")
        with col2:
            st.metric("Concepts Mastered", "24", "+3")
    
    with tabs[2]:
        st.header("Personalized Learning Path")
        subject_selection = st.multiselect(
            "Select Subjects to Focus On",
            ['Math', 'Physics', 'Chemistry']
        )
        
        if subject_selection:
            st.write("Recommended Learning Path:")
            for subject in subject_selection:
                st.write(f"📚 {subject}")
                steps = [
                    f"Step 1: Master core concepts in {subject}",
                    f"Step 2: Practice problem-solving in {subject}",
                    f"Step 3: Deep dive into advanced topics in {subject}"
                ]
                for step in steps:
                    st.write(f"   • {step}")

if __name__ == "__main__":
    main()
