import streamlit as st
from typing import Dict, Any

def render_kpi_metrics(stats: Dict[str, Any]):
    """
    Renders high-impact KPI summary cards styled for CSP Academic & Community Tourism standards.
    """
    total_trips = stats.get("total_trips", 3)
    total_budget = stats.get("total_budget", 17950)
    heritage_sites = stats.get("heritage_sites", 16)
    group_rooms = stats.get("group_rooms", 2)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="card" style="text-align: center; border-top: 4px solid #2563eb; padding: 18px 12px; margin-bottom: 12px;">
            <div style="font-size: 1.8rem; margin-bottom: 2px;">✈️</div>
            <div style="font-size: 1.8rem; font-weight: 800; color: #1e3a8a;">{total_trips}</div>
            <div style="font-size: 0.82rem; font-weight: 600; color: #64748b; text-transform: uppercase;">Trips Planned</div>
            <div style="font-size: 0.72rem; color: #16a34a; font-weight: 600; margin-top: 4px;">Active Portfolio</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card" style="text-align: center; border-top: 4px solid #059669; padding: 18px 12px; margin-bottom: 12px;">
            <div style="font-size: 1.8rem; margin-bottom: 2px;">💰</div>
            <div style="font-size: 1.8rem; font-weight: 800; color: #059669;">₹{total_budget:,.0f}</div>
            <div style="font-size: 0.82rem; font-weight: 600; color: #64748b; text-transform: uppercase;">Tracked Budget</div>
            <div style="font-size: 0.72rem; color: #059669; font-weight: 600; margin-top: 4px;">Student Optimized</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="card" style="text-align: center; border-top: 4px solid #d97706; padding: 18px 12px; margin-bottom: 12px;">
            <div style="font-size: 1.8rem; margin-bottom: 2px;">🏛️</div>
            <div style="font-size: 1.8rem; font-weight: 800; color: #d97706;">{heritage_sites}</div>
            <div style="font-size: 0.82rem; font-weight: 600; color: #64748b; text-transform: uppercase;">Heritage Sites</div>
            <div style="font-size: 0.72rem; color: #d97706; font-weight: 600; margin-top: 4px;">UNESCO & Local</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="card" style="text-align: center; border-top: 4px solid #7c3aed; padding: 18px 12px; margin-bottom: 12px;">
            <div style="font-size: 1.8rem; margin-bottom: 2px;">👥</div>
            <div style="font-size: 1.8rem; font-weight: 800; color: #7c3aed;">{group_rooms}</div>
            <div style="font-size: 0.82rem; font-weight: 600; color: #64748b; text-transform: uppercase;">Group Rooms</div>
            <div style="font-size: 0.72rem; color: #7c3aed; font-weight: 600; margin-top: 4px;">Collaborative Hub</div>
        </div>
        """, unsafe_allow_html=True)
