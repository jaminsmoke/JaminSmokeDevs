"""
HEFEST - DASHBOARD ADMIN V3 ULTRA-MODERNO
Rediseño completo del dashboard administrativo con arquitectura visual V3
Sin dependencias del sistema antiguo, componentes modernos desde cero
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QScrollArea,
    QTabWidget,
    QPushButton,
    QGridLayout,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
import logging
from datetime import datetime

# Importar el nuevo sistema ultra-moderno desde la carpeta de componentes específicos
from .components.dashboard_metric_components import (
    UltraModernTheme,
    UltraModernDashboard,
    UltraModernCard,
    UltraModernMetricCard,
    UltraModernBaseWidget,
)

# Importar componente especializado para hostelería
from .components.hospitality_metric_card import HospitalityMetricCard

# Importar el DataManager centralizado
from utils.real_data_manager import RealDataManager

# Importar lógica administrativa para métricas reales
from utils.administrative_logic_manager import AdministrativeLogicManager

# Constantes para estilos y períodos
ICON_STYLE_LARGE = "font-size: 24px; margin-right: 8px;"
ICON_STYLE_MEDIUM = "font-size: 18px;"
PERIOD_7_DAYS = "7 días"
PERIOD_LAST_MONTH = "último mes"

# Importar utilidad de compatibilidad CSS para PyQt6
from utils.qt_css_compat import convert_to_qt_compatible_css, apply_qt_workarounds

logger = logging.getLogger(__name__)


class UltraModernAdminDashboard(UltraModernBaseWidget):
    """Dashboard administrativo ultra-moderno V3"""    # Señales para comunicación con la ventana principal
    metric_selected = pyqtSignal(str, dict)  # título, datos
    action_requested = pyqtSignal(str)  # acción

    def __init__(self, auth_service=None, db_manager=None, parent=None):
        super().__init__(parent)
        self.theme = UltraModernTheme()

        # Servicios compatibles con la aplicación principal
        self.auth_service = auth_service
        self.db_manager = db_manager

        # DataManager centralizado para obtener SOLO datos reales
        self.data_manager = RealDataManager(db_manager)

        # Manager de lógica administrativa para métricas con objetivos y tendencias reales
        self.admin_logic = AdministrativeLogicManager(db_manager)

        self.metric_cards = []  # Lista de tarjetas de métricas

        self.setup_admin_dashboard()
        self.setup_admin_features()
        self.setup_centralized_data_refresh()
        
        logger.info(
            "Dashboard Admin V3 Ultra-Moderno inicializado con DataManager centralizado"
        )

    def setup_admin_dashboard(self):
        """Configurar estructura del dashboard administrativo"""
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(self.theme.SPACING["lg"])

        # Header del dashboard
        header = self.create_dashboard_header()
        main_layout.addWidget(header)

        # Contenido principal con tabs
        content_tabs = self.create_admin_tabs()
        main_layout.addWidget(content_tabs, 1)  # Expandir

        # Footer con información de estado
        footer = self.create_dashboard_footer()
        main_layout.addWidget(footer)
        # Styling del dashboard con fondo sofisticado y textura sutil        # Aplicar estilos base compatibles con PyQt6
        base_style = f"""
            UltraModernAdminDashboard {{
                background-color: {self.theme.COLORS['gray_50']};
                border: none;
                margin: 0px;
                padding: 0px;
            }}
        """

        # Convertir a CSS compatible con Qt y aplicar
        compatible_style = convert_to_qt_compatible_css(base_style)
        self.setStyleSheet(compatible_style)

    def create_dashboard_header(self):
        """Crear header del dashboard"""
        header = UltraModernBaseWidget()
        header.setFixedHeight(100)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 16, 20, 16)

        # Título principal
        title_layout = QVBoxLayout()

        main_title = QLabel("Dashboard Administrativo")
        main_title_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        main_title_font.setPointSize(self.theme.TYPOGRAPHY["text_5xl"])
        main_title_font.setWeight(self.theme.TYPOGRAPHY["font_bold"])
        main_title.setFont(main_title_font)
        main_title.setStyleSheet(f"color: {self.theme.COLORS['gray_900']};")

        subtitle = QLabel("Sistema de gestión ultra-moderno V3")
        subtitle_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        subtitle_font.setPointSize(self.theme.TYPOGRAPHY["text_lg"])
        subtitle_font.setWeight(self.theme.TYPOGRAPHY["font_normal"])
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet(f"color: {self.theme.COLORS['gray_600']};")

        title_layout.addWidget(main_title)
        title_layout.addWidget(subtitle)

        # Botones de acción rápida
        actions_layout = QHBoxLayout()

        action_buttons = [
            ("🔄 Actualizar", "refresh"),
            ("⚙️ Configurar", "settings"),
            ("📊 Reportes", "reports"),
            ("🔔 Alertas", "alerts"),
        ]

        for text, action in action_buttons:
            btn = QPushButton(text)
            btn.setStyleSheet(
                f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 {self.theme.COLORS['blue_500']},
                        stop:1 {self.theme.COLORS['blue_600']});
                    color: {self.theme.COLORS['white']};
                    border: none;
                    border-radius: {self.theme.RADIUS['md']}px;
                    padding: {self.theme.SPACING['sm']}px {self.theme.SPACING['md']}px;
                    font-size: {self.theme.TYPOGRAPHY['text_sm']}px;
                    font-weight: {self.theme.TYPOGRAPHY['font_medium'].value};
                    min-width: 100px;
                }}
                QPushButton:hover {{
                    background: {self.theme.COLORS['blue_600']};
                }}
                QPushButton:pressed {{
                    background: {self.theme.COLORS['blue_700']};
                }}
            """
            )
            btn.clicked.connect(lambda checked, a=action: self.action_requested.emit(a))
            actions_layout.addWidget(btn)

        # Layout del header
        layout.addLayout(title_layout)
        layout.addStretch()
        layout.addLayout(actions_layout)

        # Styling del header
        header.setStyleSheet(
            f"""
            UltraModernBaseWidget {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.theme.COLORS['white']},
                    stop:1 {self.theme.COLORS['blue_50']});
                border: 1px solid {self.theme.COLORS['blue_200']};
                border-radius: {self.theme.RADIUS['xl']}px;
            }}
        """
        )

        header.add_shadow("md")

        return header

    def create_admin_tabs(self):
        """Crear tabs administrativos"""
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet(
            f"""
            QTabWidget::pane {{
                border: 1px solid {self.theme.COLORS['gray_200']};
                border-top: none;
                background: {self.theme.COLORS['white']};
                border-bottom-left-radius: {self.theme.RADIUS['lg']}px;
                border-bottom-right-radius: {self.theme.RADIUS['lg']}px;
                margin-top: -1px;
            }}
            QTabBar::tab {{
                background: {self.theme.COLORS['gray_100']};
                color: {self.theme.COLORS['gray_700']};
                padding: 16px 24px;
                margin-right: 2px;
                margin-bottom: 0px;
                border: 1px solid {self.theme.COLORS['gray_200']};
                border-bottom: none;
                border-top-left-radius: {self.theme.RADIUS['lg']}px;
                border-top-right-radius: {self.theme.RADIUS['lg']}px;
                font-size: {self.theme.TYPOGRAPHY['text_base']}px;
                font-weight: {self.theme.TYPOGRAPHY['font_medium'].value};
                min-width: 120px;
            }}
            QTabBar::tab:selected {{
                background: {self.theme.COLORS['white']};
                color: {self.theme.COLORS['blue_600']};
                border: 1px solid {self.theme.COLORS['gray_200']};
                border-bottom: 1px solid {self.theme.COLORS['white']};
                font-weight: {self.theme.TYPOGRAPHY['font_semibold'].value};
                margin-bottom: -1px;
            }}
            QTabBar::tab:hover:!selected {{
                background: {self.theme.COLORS['blue_50']};
                color: {self.theme.COLORS['blue_700']};
                border-color: {self.theme.COLORS['blue_200']};
            }}
        """
        )

        # Tab 1: Métricas Principales
        self.metrics_tab = self.create_metrics_tab()
        tab_widget.addTab(self.metrics_tab, "📊 Métricas")

        # Tab 2: Análisis Avanzado
        self.analytics_tab = self.create_analytics_tab()
        tab_widget.addTab(self.analytics_tab, "📈 Análisis")

        # Tab 3: Gestión de Sistema
        self.system_tab = self.create_system_tab()
        tab_widget.addTab(self.system_tab, "⚙️ Sistema")

        return tab_widget

    def create_metrics_tab(self):
        """Crear tab de métricas principales con estructura mejorada"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)

        # Contenedor principal con estilo similar a las otras pestañas
        main_card = UltraModernCard(padding=24)
        # Crear sub-pestañas para métricas
        metrics_tab_widget = QTabWidget()
        metrics_tab_widget.setStyleSheet(
            f"""
            QTabWidget::pane {{
                border: 2px solid {self.theme.COLORS['gray_200']};
                background: {self.theme.COLORS['gray_50']};
                border-top-left-radius: 0px;
                border-top-right-radius: {self.theme.RADIUS['md']}px;
                border-bottom-left-radius: {self.theme.RADIUS['md']}px;
                border-bottom-right-radius: {self.theme.RADIUS['md']}px;
                margin-top: 0px;
                padding: 0px;
            }}
            QTabBar::tab {{
                background: {self.theme.COLORS['gray_100']};
                color: {self.theme.COLORS['gray_600']};
                padding: 12px 20px;
                margin-right: 0px;
                margin-bottom: -1px;
                margin-left: 0px;
                border: 1px solid {self.theme.COLORS['gray_200']};
                border-bottom: none;
                border-top-left-radius: {self.theme.RADIUS['md']}px;
                border-top-right-radius: {self.theme.RADIUS['md']}px;
                font-size: {self.theme.TYPOGRAPHY['text_sm']}px;
                font-weight: {self.theme.TYPOGRAPHY['font_medium'].value};
                min-width: 100px;
            }}
            QTabBar::tab:first {{
                margin-left: 0px;
                border-top-left-radius: 0px;
                border-top-right-radius: {self.theme.RADIUS['md']}px;
            }}
            QTabBar::tab:!first {{
                margin-left: 0px;
            }}
            QTabBar::tab:selected {{
                background: {self.theme.COLORS['gray_50']};                color: {self.theme.COLORS['blue_600']};
                border: 1px solid {self.theme.COLORS['gray_200']};
                border-bottom: 1px solid {self.theme.COLORS['gray_50']};
                font-weight: {self.theme.TYPOGRAPHY['font_semibold'].value};
            }}
            QTabBar::tab:hover:!selected {{
                background: {self.theme.COLORS['blue_50']};
                color: {self.theme.COLORS['blue_700']};
                border-color: {self.theme.COLORS['blue_200']};
            }}
            QTabBar {{
                qproperty-drawBase: 0;
            }}
        """
        )
        # Sub-pestaña 1: Vista Resumen
        summary_tab = self.create_summary_view()
        metrics_tab_widget.addTab(summary_tab, "📊 Resumen")

        # Sub-pestaña 2: Vista Detallada
        detailed_tab = self.create_detailed_view()
        metrics_tab_widget.addTab(detailed_tab, "📈 Detalles")

        # Sub-pestaña 3: Vista Comparativa
        comparison_tab = self.create_comparison_view()
        metrics_tab_widget.addTab(comparison_tab, "🔄 Comparar")

        main_card.main_layout.addWidget(metrics_tab_widget)
        layout.addWidget(main_card)

        return widget

    def create_summary_view(self):
        """📊 RESUMEN EJECUTIVO - Vista de alto nivel para decisiones rápidas"""
        # Widget principal con scroll para manejar contenido extenso
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet(
            f"""
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QScrollBar:vertical {{
                background: {self.theme.COLORS['gray_100']};
                width: 8px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background: {self.theme.COLORS['gray_400']};
                border-radius: 4px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {self.theme.COLORS['gray_500']};
            }}
        """
        )

        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)  # Incrementar márgenes
        layout.setSpacing(32)  # Incrementar espaciado entre secciones principales
        # Header ejecutivo con título y controles
        header_layout = QHBoxLayout()
        # Título con icono distintivo
        title_container = QHBoxLayout()
        title_icon = QLabel("📊")
        title_icon.setStyleSheet(ICON_STYLE_LARGE)

        title_label = QLabel("Vista Ejecutiva")
        title_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        title_font.setPointSize(self.theme.TYPOGRAPHY["text_2xl"])
        title_font.setWeight(self.theme.TYPOGRAPHY["font_bold"])
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {self.theme.COLORS['gray_900']};")

        subtitle_label = QLabel("Métricas críticas para decisiones rápidas")
        subtitle_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        subtitle_font.setPointSize(self.theme.TYPOGRAPHY["text_sm"])
        subtitle_font.setWeight(self.theme.TYPOGRAPHY["font_normal"])
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet(
            f"color: {self.theme.COLORS['gray_600']}; margin-top: 4px;"
        )

        title_v_layout = QVBoxLayout()
        title_v_layout.addWidget(title_label)
        title_v_layout.addWidget(subtitle_label)
        title_v_layout.setSpacing(2)

        title_container.addWidget(title_icon)
        title_container.addLayout(title_v_layout)
        title_container.addStretch()
        # Botones de acción rápida
        action_buttons_layout = QHBoxLayout()

        refresh_btn = QPushButton("🔄 Actualizar")
        refresh_style = f"""
            QPushButton {{
                background: {self.theme.COLORS['blue_600']};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 500;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background: {self.theme.COLORS['blue_700']};
            }}
        """
        refresh_btn.setStyleSheet(convert_to_qt_compatible_css(refresh_style))
        export_btn = QPushButton("📊 Exportar")
        export_style = f"""
            QPushButton {{
                background: {self.theme.COLORS['gray_100']};
                color: {self.theme.COLORS['gray_700']};
                border: 1px solid {self.theme.COLORS['gray_300']};
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 500;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background: {self.theme.COLORS['gray_200']};
                border-color: {self.theme.COLORS['gray_400']};
            }}
        """
        export_btn.setStyleSheet(convert_to_qt_compatible_css(export_style))

        action_buttons_layout.addWidget(refresh_btn)
        action_buttons_layout.addWidget(export_btn)

        header_layout.addLayout(title_container)
        header_layout.addLayout(action_buttons_layout)
        layout.addLayout(header_layout)

        # Separador visual después del header
        header_separator = QFrame()
        header_separator.setFrameShape(QFrame.Shape.HLine)
        header_separator.setStyleSheet(
            f"""
            QFrame {{
                background-color: {self.theme.COLORS['gray_200']};
                max-height: 1px;
                margin: 8px 0px;
            }}
        """
        )
        layout.addWidget(header_separator)
        # KPIs críticos en grid 3x2 (6 métricas principales) con contenedor
        kpis_container = QWidget()
        kpis_container.setStyleSheet(
            """
            QWidget {
                background-color: transparent;
                margin: 16px 0px;
            }
        """
        )
        kpis_layout = QVBoxLayout(kpis_container)
        kpis_layout.setContentsMargins(0, 0, 0, 0)
        kpis_layout.setSpacing(16)

        # Título de la sección KPIs
        kpi_title = QLabel("📈 Indicadores Clave de Rendimiento")
        kpi_title_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        kpi_title_font.setPointSize(self.theme.TYPOGRAPHY["text_lg"])
        kpi_title_font.setWeight(self.theme.TYPOGRAPHY["font_semibold"])
        kpi_title.setFont(kpi_title_font)
        kpi_title.setStyleSheet(
            f"color: {self.theme.COLORS['gray_800']}; margin-bottom: 12px;"
        )
        kpis_layout.addWidget(kpi_title)
        # Grid de KPIs
        kpis_grid = QGridLayout()
        kpis_grid.setSpacing(20)  # Aumentar espaciado entre tarjetas

        # Obtener métricas administrativas reales con lógica de negocio
        logger.info("📊 Obteniendo métricas administrativas con lógica real...")
        administrative_metrics = self.admin_logic.get_administrative_metrics()

        # Convertir métricas administrativas al formato requerido por las tarjetas KPI
        executive_kpis = []
        for title, metric_data in administrative_metrics.items():
            kpi_data = {
                "title": metric_data["title"],
                "value": metric_data["value"],
                "trend": metric_data["trend"],
                "trend_direction": metric_data["trend_direction"],
                "comparison": metric_data["comparison"],
                "icon": metric_data["icon"],
                "priority": metric_data["priority"],
                "action": metric_data["action"],
                "progress": metric_data["progress"],  # Para la barra de progreso
                "target": metric_data["target"],  # Objetivo administrativo
            }
            executive_kpis.append(kpi_data)

        logger.info(
            f"✅ Cargadas {len(executive_kpis)} métricas administrativas reales"
        )

        # Crear cards KPI ejecutivos con estilo diferenciado
        for i, kpi in enumerate(executive_kpis):
            row = i // 3
            col = i % 3
            card = self.create_executive_kpi_card(kpi)
            kpis_grid.addWidget(card, row, col)

        kpis_layout.addLayout(kpis_grid)
        layout.addWidget(kpis_container)

        # Separador entre secciones
        section_separator = QFrame()
        section_separator.setFrameShape(QFrame.Shape.HLine)
        section_separator.setStyleSheet(
            f"""
            QFrame {{
                background-color: {self.theme.COLORS['gray_200']};
                max-height: 1px;
                margin: 20px 0px;
            }}
        """
        )
        layout.addWidget(section_separator)
        # Panel de alertas y notificaciones críticas con datos reales
        alerts_section = self.create_alerts_summary()
        layout.addWidget(alerts_section)

        # Separador entre secciones
        section_separator2 = QFrame()
        section_separator2.setFrameShape(QFrame.Shape.HLine)
        section_separator2.setStyleSheet(
            f"""
            QFrame {{
                background-color: {self.theme.COLORS['gray_200']};
                max-height: 1px;
                margin: 20px 0px;
            }}
        """
        )
        layout.addWidget(section_separator2)

        # Tendencias rápidas (mini gráficos) con espaciado mejorado
        trends_section = self.create_executive_trends_section()
        layout.addWidget(trends_section)

        layout.addStretch()

        # Configurar el scroll area
        scroll_area.setWidget(widget)
        return scroll_area

    def create_analytics_tab(self):
        """Crear tab de análisis avanzado"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)

        # Placeholder para análisis avanzado
        placeholder = UltraModernCard(padding=32)

        content_layout = QVBoxLayout()

        title = QLabel("Análisis Avanzado")
        title_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        title_font.setPointSize(self.theme.TYPOGRAPHY["text_4xl"])
        title_font.setWeight(self.theme.TYPOGRAPHY["font_bold"])
        title.setFont(title_font)
        title.setStyleSheet(f"color: {self.theme.COLORS['gray_900']};")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        description = QLabel("Módulo de análisis de datos avanzado en desarrollo")
        description_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        description_font.setPointSize(self.theme.TYPOGRAPHY["text_lg"])
        description.setFont(description_font)
        description.setStyleSheet(f"color: {self.theme.COLORS['gray_600']};")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)

        content_layout.addWidget(title)
        content_layout.addWidget(description)
        content_layout.addStretch()

        placeholder.main_layout.addLayout(content_layout)
        layout.addWidget(placeholder)
        return widget

    def create_detailed_view(self):
        """📈 VISTA DETALLADA - Análisis granular por categorías operativas"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        # Header detallado con filtros y controles
        header_layout = QHBoxLayout()
        # Título con icono distintivo
        title_container = QHBoxLayout()
        title_icon = QLabel("📈")
        title_icon.setStyleSheet(ICON_STYLE_LARGE)

        title_label = QLabel("Análisis Detallado")
        title_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        title_font.setPointSize(self.theme.TYPOGRAPHY["text_2xl"])
        title_font.setWeight(self.theme.TYPOGRAPHY["font_bold"])
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {self.theme.COLORS['gray_900']};")

        subtitle_label = QLabel("Métricas operativas organizadas por categorías")
        subtitle_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        subtitle_font.setPointSize(self.theme.TYPOGRAPHY["text_sm"])
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet(
            f"color: {self.theme.COLORS['gray_600']}; margin-top: 4px;"
        )

        title_v_layout = QVBoxLayout()
        title_v_layout.addWidget(title_label)
        title_v_layout.addWidget(subtitle_label)
        title_v_layout.setSpacing(2)

        title_container.addWidget(title_icon)
        title_container.addLayout(title_v_layout)
        title_container.addStretch()

        # Controles de filtro y período
        controls_layout = QHBoxLayout()

        period_btn = QPushButton("📅 Últimos 7 días")
        period_btn.setStyleSheet(
            f"""
            QPushButton {{
                background: {self.theme.COLORS['gray_100']};
                color: {self.theme.COLORS['gray_700']};
                border: 1px solid {self.theme.COLORS['gray_300']};
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 500;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background: {self.theme.COLORS['gray_200']};
                border-color: {self.theme.COLORS['gray_400']};
            }}
        """
        )

        filter_combo = QPushButton("🔍 Filtrar por: Todos")
        filter_combo.setStyleSheet(
            f"""
            QPushButton {{
                background: {self.theme.COLORS['gray_100']};
                color: {self.theme.COLORS['gray_700']};
                border: 1px solid {self.theme.COLORS['gray_300']};
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 500;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background: {self.theme.COLORS['gray_200']};
                border-color: {self.theme.COLORS['gray_400']};
            }}
        """
        )

        controls_layout.addWidget(period_btn)
        controls_layout.addWidget(filter_combo)

        header_layout.addLayout(title_container)
        header_layout.addLayout(controls_layout)
        layout.addLayout(header_layout)

        # Scroll area para métricas categorizadas
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameStyle(QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet(
            f"""
            QScrollArea {{ 
                background: transparent; 
                border: none;
            }}
            QScrollBar:vertical {{
                background: {self.theme.COLORS['gray_100']};
                width: 8px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background: {self.theme.COLORS['gray_300']};
                border-radius: 4px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {self.theme.COLORS['gray_500']};
            }}
        """
        )

        # Contenedor principal
        main_container = QWidget()
        main_container.setStyleSheet(
            f"""
            QWidget {{
                background: {self.theme.COLORS['gray_50']};
                border: none;
            }}
        """
        )
        container_layout = QVBoxLayout(main_container)
        container_layout.setSpacing(24)
        container_layout.setContentsMargins(16, 16, 16, 16)

        # CATEGORÍAS DE MÉTRICAS ORGANIZADAS
        categories = [
            {
                "title": "💰 Rendimiento Financiero",
                "description": "Métricas de ingresos, costos y rentabilidad",
                "metrics": [
                    {
                        "title": "Ingresos Totales",
                        "value": "€4,287",
                        "trend": "+8.5%",
                        "period": PERIOD_7_DAYS,
                        "icon": "💵",
                    },
                    {
                        "title": "Costo de Ventas",
                        "value": "€1,354",
                        "trend": "-2.3%",
                        "period": PERIOD_7_DAYS,
                        "icon": "🏷️",
                    },
                    {
                        "title": "Margen de Contribución",
                        "value": "68.4%",
                        "trend": "+3.2%",
                        "period": PERIOD_7_DAYS,
                        "icon": "📊",
                    },
                    {
                        "title": "ROI Promociones",
                        "value": "145%",
                        "trend": "+12%",
                        "period": PERIOD_LAST_MONTH,
                        "icon": "🎯",
                    },
                    {
                        "title": "Flujo de Caja",
                        "value": "€2,933",
                        "trend": "+5.7%",
                        "period": PERIOD_7_DAYS,
                        "icon": "💸",
                    },
                    {
                        "title": "Punto de Equilibrio",
                        "value": "82%",
                        "trend": "+4%",
                        "period": "mes actual",
                        "icon": "⚖️",
                    },
                ],
            },
            {
                "title": "👥 Experiencia del Cliente",
                "description": "Satisfacción, retención y comportamiento de clientes",
                "metrics": [
                    {
                        "title": "NPS Score",
                        "value": "72",
                        "trend": "+8",
                        "period": PERIOD_LAST_MONTH,
                        "icon": "🌟",
                    },
                    {
                        "title": "Tiempo Esp. Promedio",
                        "value": "4.2min",
                        "trend": "-8%",
                        "period": PERIOD_7_DAYS,
                        "icon": "⏰",
                    },
                    {
                        "title": "Tasa de Retención",
                        "value": "84%",
                        "trend": "+2.1%",
                        "period": PERIOD_LAST_MONTH,
                        "icon": "🔄",
                    },
                    {
                        "title": "Quejas Resueltas",
                        "value": "96%",
                        "trend": "+4%",
                        "period": PERIOD_7_DAYS,
                        "icon": "✅",
                    },
                    {
                        "title": "Clientes Recurrentes",
                        "value": "67%",
                        "trend": "+5.3%",
                        "period": PERIOD_LAST_MONTH,
                        "icon": "👤",
                    },
                    {
                        "title": "Valoración Media",
                        "value": "4.6★",
                        "trend": "+0.2",
                        "period": PERIOD_7_DAYS,
                        "icon": "⭐",
                    },
                ],
            },
            {
                "title": "⚡ Eficiencia Operativa",
                "description": "Productividad, recursos y procesos internos",
                "metrics": [
                    {
                        "title": "Productividad/Hora",
                        "value": "€47",
                        "trend": "+9.1%",
                        "period": PERIOD_7_DAYS,
                        "icon": "📈",
                    },
                    {
                        "title": "Rotación Personal",
                        "value": "8%",
                        "trend": "-3%",
                        "period": "último trimestre",
                        "icon": "🔄",
                    },
                    {
                        "title": "Utilización Mesas",
                        "value": "78%",
                        "trend": "+6%",
                        "period": PERIOD_7_DAYS,
                        "icon": "🪑",
                    },
                    {
                        "title": "Tiempo Ciclo Pedido",
                        "value": "12min",
                        "trend": "-15%",
                        "period": PERIOD_7_DAYS,
                        "icon": "🕒",
                    },
                    {
                        "title": "Eficiencia Energética",
                        "value": "92%",
                        "trend": "+2%",
                        "period": PERIOD_LAST_MONTH,
                        "icon": "⚡",
                    },
                    {
                        "title": "Desperdicio Alimentario",
                        "value": "3.2%",
                        "trend": "-18%",
                        "period": PERIOD_7_DAYS,
                        "icon": "♻️",
                    },
                ],
            },
            {
                "title": "📦 Gestión de Inventario",
                "description": "Stock, rotación y control de merma",
                "metrics": [
                    {
                        "title": "Rotación Inventario",
                        "value": "12.4x",
                        "trend": "+8%",
                        "period": PERIOD_LAST_MONTH,
                        "icon": "🔄",
                    },
                    {
                        "title": "Stock Out Events",
                        "value": "2",
                        "trend": "-50%",
                        "period": PERIOD_7_DAYS,
                        "icon": "📉",
                    },
                    {
                        "title": "Margen Inventario",
                        "value": "€8,450",
                        "trend": "+3.7%",
                        "period": "actual",
                        "icon": "💰",
                    },
                    {
                        "title": "Productos Críticos",
                        "value": "7",
                        "trend": "+2",
                        "period": "actual",
                        "icon": "⚠️",
                    },
                    {
                        "title": "Tasa de Merma",
                        "value": "2.1%",
                        "trend": "-12%",
                        "period": PERIOD_7_DAYS,
                        "icon": "📉",
                    },
                    {
                        "title": "Días de Stock",
                        "value": "21",
                        "trend": "-2",
                        "period": "promedio",
                        "icon": "📅",
                    },
                ],
            },
        ]

        # Crear secciones por categoría
        for category in categories:
            category_section = self.create_detailed_category_section(category)
            container_layout.addWidget(category_section)

        container_layout.addStretch()
        scroll_area.setWidget(main_container)
        layout.addWidget(scroll_area)

        return widget

    def create_comparison_view(self):
        """🔄 VISTA COMPARATIVA - Análisis de tendencias y comparaciones temporales"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        # Header comparativo con selección de períodos
        header_layout = QHBoxLayout()
        # Título con icono distintivo
        title_container = QHBoxLayout()
        title_icon = QLabel("🔄")
        title_icon.setStyleSheet(ICON_STYLE_LARGE)

        title_label = QLabel("Análisis Comparativo")
        title_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        title_font.setPointSize(self.theme.TYPOGRAPHY["text_2xl"])
        title_font.setWeight(self.theme.TYPOGRAPHY["font_bold"])
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {self.theme.COLORS['gray_900']};")

        subtitle_label = QLabel("Comparación de períodos y análisis de tendencias")
        subtitle_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        subtitle_font.setPointSize(self.theme.TYPOGRAPHY["text_sm"])
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet(
            f"color: {self.theme.COLORS['gray_600']}; margin-top: 4px;"
        )

        title_v_layout = QVBoxLayout()
        title_v_layout.addWidget(title_label)
        title_v_layout.addWidget(subtitle_label)
        title_v_layout.setSpacing(2)

        title_container.addWidget(title_icon)
        title_container.addLayout(title_v_layout)
        title_container.addStretch()

        # Controles de comparación
        comparison_controls = QHBoxLayout()

        # Selector de período base
        base_period_btn = QPushButton("📅 Período Base: Esta Semana")
        base_period_btn.setStyleSheet(
            f"""
            QPushButton {{
                background: {self.theme.COLORS['blue_100']};
                color: {self.theme.COLORS['blue_700']};
                border: 2px solid {self.theme.COLORS['blue_300']};
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background: {self.theme.COLORS['blue_200']};
                border-color: {self.theme.COLORS['blue_400']};
            }}
        """
        )

        # Selector de período comparación
        compare_period_btn = QPushButton("📊 Comparar con: Semana Anterior")
        compare_period_btn.setStyleSheet(
            f"""
            QPushButton {{
                background: {self.theme.COLORS['green_100']};
                color: {self.theme.COLORS['green_700']};
                border: 2px solid {self.theme.COLORS['green_300']};
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background: {self.theme.COLORS['green_200']};
                border-color: {self.theme.COLORS['green_400']};
            }}
        """
        )

        # Botón de actualización
        refresh_btn = QPushButton("🔄 Actualizar Comparación")
        refresh_btn.setStyleSheet(
            f"""
            QPushButton {{
                background: {self.theme.COLORS['gray_600']};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 500;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background: {self.theme.COLORS['gray_700']};
            }}
        """
        )

        comparison_controls.addWidget(base_period_btn)
        comparison_controls.addWidget(compare_period_btn)
        comparison_controls.addWidget(refresh_btn)

        header_layout.addLayout(title_container)
        header_layout.addLayout(comparison_controls)
        layout.addLayout(header_layout)

        # Métricas comparativas principales en cards
        main_comparison_section = self.create_main_comparison_cards()
        layout.addWidget(main_comparison_section)

        # Análisis de tendencias detallado
        trends_section = self.create_trends_analysis_section()
        layout.addWidget(trends_section)

        # Insights y recomendaciones
        insights_section = self.create_insights_section()
        layout.addWidget(insights_section)

        layout.addStretch()
        return widget

    def create_system_tab(self):
        """Crear tab de gestión del sistema"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)

        # Información del sistema
        system_info_card = UltraModernCard(padding=24)

        info_layout = QVBoxLayout()

        title = QLabel("Información del Sistema")
        title_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        title_font.setPointSize(self.theme.TYPOGRAPHY["text_3xl"])
        title_font.setWeight(self.theme.TYPOGRAPHY["font_bold"])
        title.setFont(title_font)
        title.setStyleSheet(f"color: {self.theme.COLORS['gray_900']};")

        system_details = QLabel(
            f"""
        🚀 Hefest Dashboard Admin V3 Ultra-Moderno
        
        📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
        🎨 Sistema Visual: V3 Ultra-Moderno
        ⚡ Motor: PyQt6 nativo
        🔧 Estado: Operativo
        
        ✅ Características activas:
        • Dashboard con métricas en tiempo real
        • Componentes ultra-modernos sin filtros destructivos
        • Animaciones suaves y efectos visuales
        • Grid responsivo y adaptativo
        • Simulación de datos automática
        • Arquitectura modular y escalable
        """
        )

        system_details_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        system_details_font.setPointSize(self.theme.TYPOGRAPHY["text_base"])
        system_details.setFont(system_details_font)
        system_details.setStyleSheet(f"color: {self.theme.COLORS['gray_700']};")

        info_layout.addWidget(title)
        info_layout.addWidget(system_details)
        info_layout.addStretch()

        system_info_card.main_layout.addLayout(info_layout)
        layout.addWidget(system_info_card)

        return widget

    def create_dashboard_footer(self):
        """Crear footer del dashboard"""
        footer = UltraModernBaseWidget()
        footer.setFixedHeight(50)

        layout = QHBoxLayout(footer)
        layout.setContentsMargins(20, 12, 20, 12)

        # Estado del sistema
        status_label = QLabel("🟢 Sistema Operativo")
        status_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        status_font.setPointSize(self.theme.TYPOGRAPHY["text_sm"])
        status_font.setWeight(self.theme.TYPOGRAPHY["font_medium"])
        status_label.setFont(status_font)
        status_label.setStyleSheet(f"color: {self.theme.COLORS['green_600']};")

        # Información de actualización
        update_label = QLabel(
            f"Última actualización: {datetime.now().strftime('%H:%M:%S')}"
        )
        update_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        update_font.setPointSize(self.theme.TYPOGRAPHY["text_xs"])
        update_label.setFont(update_font)
        update_label.setStyleSheet(f"color: {self.theme.COLORS['gray_500']};")

        layout.addWidget(status_label)
        layout.addStretch()
        layout.addWidget(update_label)

        # Styling del footer
        footer.setStyleSheet(
            f"""
            UltraModernBaseWidget {{
                background: {self.theme.COLORS['gray_100']};
                border: 1px solid {self.theme.COLORS['gray_200']};
                border-radius: {self.theme.RADIUS['md']}px;
            }}        """
        )

        return footer

    def setup_admin_features(self):
        """Configurar características administrativas y conexiones de datos reales"""
        logger.info("Configurando características administrativas avanzadas")

        # Configurar actualización automática de datos reales
        self.setup_data_refresh()

        # Hacer una primera carga de datos reales
        logger.info("📊 Realizando carga inicial de datos reales")
        self.data_manager.fetch_all_real_data()

        logger.info("✅ Características administrativas configuradas con datos reales")

    def refresh_admin_data(self):
        """
        Actualizar manualmente todos los datos administrativos
        Método requerido por la interfaz del dashboard
        """
        logger.info("Actualizando datos administrativos manualmente")
        if hasattr(self, "data_manager"):
            self.data_manager.fetch_all_real_data()
        else:
            logger.warning("DataManager no disponible para actualización manual")

    def setup_data_refresh(self):
        """Configurar DataManager centralizado - Las tarjetas se auto-gestionan"""
        # NOTA: Ya no conectamos señales del DataManager al dashboard
        # Las tarjetas HospitalityMetricCard se conectan directamente al RealDataManager

        # Iniciar monitoreo centralizado
        self.data_manager.start_monitoring(5000)  # 5 segundos
        logger.info(
            "DataManager centralizado configurado (5s) - Tarjetas auto-gestionadas"
        )

    def setup_centralized_data_refresh(self):
        """Alias para compatibilidad"""
        self.setup_data_refresh()

    def on_metric_selected(self, title, data):
        """Manejar selección de métrica"""
        logger.info(f"Métrica seleccionada: {title}")
        self.metric_selected.emit(title, data)

    def on_action_requested(self, action):
        """Manejar solicitud de acción"""
        logger.info(f"Acción solicitada: {action}")
        self.action_requested.emit(action)

    def resizeEvent(self, event):
        """
        Manejo responsivo del dashboard
        Adapta el número de columnas según el ancho disponible
        """
        super().resizeEvent(event)
        logger.debug(
            f"Dashboard redimensionado a {event.size().width()}x{event.size().height()}"
        )

    def _create_metric_cards_from_real_data(self, metrics_layout):
        """Crear tarjetas de métricas usando componentes especializados auto-gestionados"""
        logger.info("🔄 Creando tarjetas auto-gestionadas con HospitalityMetricCard")

        # Lista de métricas de hostelería que se auto-gestionan
        hospitality_metrics = [
            "ventas_diarias",
            "comandas_activas",
            "mesas_ocupadas",
            "ticket_promedio",
            "satisfaccion_cliente",
            "tiempo_servicio",
            "rotacion_mesas",
            "inventario_bebidas",
            "margen_bruto",
        ]

        # Crear tarjetas especializadas que se auto-gestionan completamente
        for i, metric_type in enumerate(hospitality_metrics):
            logger.debug(f"📋 Creando tarjeta auto-gestionada: {metric_type}")

            # Crear tarjeta especializada que se conecta directamente al RealDataManager
            card = HospitalityMetricCard(
                metric_type=metric_type,
                data_manager=self.data_manager,  # La tarjeta se gestiona sola
                parent=self,
            )

            # Conectar señales solo para interacción con el dashboard
            card.clicked.connect(
                lambda checked, mtype=metric_type: self.metric_selected.emit(
                    mtype, {"type": mtype}
                )
            )

            # Agregar al layout (grid responsivo)
            row = i // 3  # 3 columnas por defecto
            col = i % 3
            metrics_layout.addWidget(card, row, col)

            # Solo guardar referencia para limpieza, NO para gestión de datos
            self.metric_cards.append(card)
        logger.info(f"✅ Creadas {len(self.metric_cards)} tarjetas auto-gestionadas")
        logger.info(
            "📌 Dashboard liberado de lógica de KPIs - Componentes completamente autónomos"
        )

    def _create_detailed_metric_cards_from_real_data(self, metrics_layout):
        """Crear tarjetas detalladas usando componentes especializados auto-gestionados"""
        logger.info("🔄 Creando vista detallada con tarjetas auto-gestionadas")

        # Lista extendida de métricas de hostelería para vista detallada
        detailed_hospitality_metrics = [
            "ventas_diarias",
            "comandas_activas",
            "mesas_ocupadas",
            "ticket_promedio",
            "satisfaccion_cliente",
            "tiempo_servicio",
            "rotacion_mesas",
            "inventario_bebidas",
            "margen_bruto",
            "ocupacion",
            "coste_medio",
            "reservas_activas",
            "tiempo_espera",
        ]

        # Crear tarjetas especializadas detalladas que se auto-gestionan completamente
        for i, metric_type in enumerate(detailed_hospitality_metrics):
            logger.debug(f"📋 Creando tarjeta detallada auto-gestionada: {metric_type}")

            # Crear tarjeta especializada que se conecta directamente al RealDataManager
            card = HospitalityMetricCard(
                metric_type=metric_type,
                data_manager=self.data_manager,  # La tarjeta se gestiona sola
                parent=self,
            )

            # Conectar señales solo para interacción con el dashboard
            card.clicked.connect(
                lambda checked, mtype=metric_type: self.metric_selected.emit(
                    mtype, {"type": mtype}
                )
            )

            # Agregar al layout (grid responsivo para vista detallada - 4 columnas)
            row = i // 4  # 4 columnas para vista detallada
            col = i % 4
            metrics_layout.addWidget(card, row, col)
            # Solo guardar referencia para limpieza, NO para gestión de datos
            self.metric_cards.append(card)

        logger.info(
            f"✅ Creadas {len(detailed_hospitality_metrics)} tarjetas detalladas auto-gestionadas"
        )
        logger.info(
            "📌 Vista detallada liberada de lógica de KPIs - Componentes completamente autónomos"
        )

    def cleanup(self):
        """Limpiar recursos y cerrar conexiones al cerrar el dashboard"""
        try:
            logger.info("🧹 Iniciando limpieza del dashboard")

            # Limpiar tarjetas auto-gestionadas
            for card in self.metric_cards:
                if hasattr(card, "cleanup"):
                    card.cleanup()

            # Detener el RealDataManager
            if self.data_manager:
                self.data_manager.stop_monitoring()
                logger.debug("RealDataManager detenido")            # Limpiar lista de tarjetas
            self.metric_cards.clear()

            logger.info("✅ Limpieza del dashboard completada")
            
        except Exception as e:
            logger.warning(f"Error durante limpieza del dashboard: {e}")

    def __del__(self):
        """Destructor para asegurar limpieza de recursos"""
        try:
            self.cleanup()
        except Exception:
            pass  # Evitar errores en destructor

    def create_executive_kpi_card(self, kpi_data):
        """Crear tarjeta KPI ejecutiva usando UltraModernMetricCard con datos administrativos reales"""
        # Crear la tarjeta con todos los datos administrativos reales
        card = UltraModernMetricCard(
            title=kpi_data.get("title", "Métrica"),
            value=str(kpi_data.get("value", "0")),
            unit="",  # Las unidades ya están incluidas en el valor
            trend=kpi_data.get("trend", "0%"),
            metric_type=kpi_data.get("priority", "medium"),
            icon=kpi_data.get("icon", "📊"),
            target=str(kpi_data.get("target", "100")),  # Usar objetivo real
        )
        # CRUCIAL: Actualizar con los datos administrativos reales después de la creación
        # Esto asegura que las barras de progreso y tendencias reflejen datos reales
        card.update_metric_data(
            value=kpi_data.get("value"),
            trend=kpi_data.get("trend"),
            target=kpi_data.get("target_numeric", 100),  # Valor numérico del objetivo
            progress_percentage=kpi_data.get(
                "progress", 50
            ),  # Porcentaje administrativo real
        )

        logger.info(
            f"📊 Configurando datos administrativos reales para {kpi_data.get('title')}:"
        )
        logger.info(f"   - Valor: {kpi_data.get('value')}")
        logger.info(
            f"   - Tendencia: {kpi_data.get('trend')} ({kpi_data.get('trend_direction')})"
        )
        logger.info(f"   - Progreso: {kpi_data.get('progress', 0):.1f}%")
        logger.info(f"   - Objetivo: {kpi_data.get('target')}")
        # Ajustar tamaño para el grid - AUMENTADO para mejor visualización
        card.setMinimumSize(280, 180)  # Aumentado de 200x140 a 280x180
        card.setMaximumSize(400, 240)  # Aumentado de 350x180 a 400x240

        # Aplicar estilo específico basado en prioridad
        priority = kpi_data.get("priority", "medium")
        priority_styles = {
            "critical": {"border": "#DC2626", "bg": "#FEF2F2"},
            "urgent": {"border": "#EA580C", "bg": "#FFF7ED"},
            "high": {"border": "#2563EB", "bg": "#EFF6FF"},
            "medium": {"border": "#16A34A", "bg": "#F0FDF4"},
            "good": {"border": "#0EA5E9", "bg": "#F0F9FF"},
        }

        style = priority_styles.get(priority, priority_styles["medium"])
        card.setStyleSheet(
            f"""
            UltraModernMetricCard {{
                border: 2px solid {style["border"]};
                background: {style["bg"]};
                border-radius: 12px;
                padding: 16px;
                min-height: 180px;
            }}
            UltraModernMetricCard:hover {{
                border-color: {style["border"]};
                background: white;
            }}            UltraModernMetricCard QLabel {{
                background: transparent;
            }}        """
        )

        return card

    def create_alerts_summary(self):
        """Crear resumen de alertas administrativas usando datos reales"""
        try:
            # Usar el componente de alertas administrativas real
            from .components.administrative_alerts_component import (
                AdministrativeAlertsComponent,
            )

            alerts_component = AdministrativeAlertsComponent(parent=self)

            # Configurar tamaño del componente
            alerts_component.setMaximumHeight(200)
            alerts_component.setMinimumHeight(120)

            logger.info("✅ Componente de alertas administrativas reales creado")
            return alerts_component

        except Exception as e:
            logger.error(f"Error creando componente de alertas: {e}")

            # Fallback: Mostrar mensaje simple de error
            error_widget = QWidget()
            error_layout = QVBoxLayout(error_widget)
            error_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            error_layout.setSpacing(8)

            error_label = QLabel("⚠️ Alertas temporalmente no disponibles")
            error_label.setStyleSheet("color: #6B7280; font-size: 14px;")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            error_layout.addWidget(error_label)

            return error_widget

    def create_executive_alerts_panel(self):
        """Panel de alertas críticas para vista ejecutiva"""
        alerts_card = UltraModernCard(padding=24)  # Aumentar padding
        alerts_card.setMinimumHeight(220)  # Altura mínima en lugar de máxima
        alerts_card.setMaximumHeight(280)  # Altura máxima más generosa

        # Título del panel con mejor espaciado
        title_layout = QHBoxLayout()
        title_layout.setSpacing(8)
        title_icon = QLabel("🚨")
        title_icon.setStyleSheet(ICON_STYLE_MEDIUM)

        title_label = QLabel("Alertas Críticas")
        title_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        title_font.setPointSize(self.theme.TYPOGRAPHY["text_lg"])
        title_font.setWeight(self.theme.TYPOGRAPHY["font_semibold"])
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {self.theme.COLORS['gray_900']};")

        title_layout.addWidget(title_icon)
        title_layout.addWidget(title_label)
        title_layout.addStretch()

        # Lista de alertas con espaciado mejorado
        alerts_layout = QVBoxLayout()
        alerts_layout.setSpacing(12)  # Incrementar espaciado entre alertas

        # Ejemplos de alertas críticas
        critical_alerts = [
            {
                "type": "critical",
                "message": "Stock crítico: Aceite de oliva (2 unidades)",
                "icon": "📦",
            },
            {
                "type": "warning",
                "message": "Tiempo promedio de servicio aumentó 15%",
                "icon": "⏱️",
            },
            {
                "type": "info",
                "message": "Nueva reseña de 5 estrellas recibida",
                "icon": "⭐",
            },
        ]

        for alert in critical_alerts:
            alert_item = self.create_alert_item(alert)
            alerts_layout.addWidget(alert_item)

        alerts_card.main_layout.addLayout(title_layout)
        alerts_card.main_layout.addSpacing(16)  # Espaciado entre título y contenido
        alerts_card.main_layout.addLayout(alerts_layout)

        return alerts_card

    def create_alert_item(self, alert_data):
        """Crear item individual de alerta"""
        item_widget = QWidget()
        item_widget.setMinimumHeight(50)  # Altura mínima para evitar cortes
        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(16, 12, 16, 12)  # Márgenes más generosos
        item_layout.setSpacing(10)  # Espaciado entre icono y texto
        # Icono de alerta
        icon_label = QLabel(alert_data.get("icon", "ℹ️"))
        icon_label.setStyleSheet(ICON_STYLE_MEDIUM)  # Icono ligeramente más grande
        icon_label.setAlignment(Qt.AlignmentFlag.AlignTop)  # Alinear al tope

        # Mensaje de alerta con wrap
        message_label = QLabel(alert_data.get("message", "Sin mensaje"))
        message_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        message_font.setPointSize(12)  # Aumentar tamaño de fuente
        message_label.setFont(message_font)
        message_label.setWordWrap(True)  # CLAVE: Permitir texto en múltiples líneas
        message_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        # Color según tipo de alerta
        alert_type = alert_data.get("type", "info")
        if alert_type == "critical":
            bg_color = "#FEF2F2"
            text_color = "#DC2626"
            border_color = "#FECACA"
        elif alert_type == "warning":
            bg_color = "#FFFBEB"
            text_color = "#D97706"
            border_color = "#FED7AA"
        else:
            bg_color = "#EFF6FF"
            text_color = "#2563EB"
            border_color = "#BFDBFE"

        message_label.setStyleSheet(
            f"color: {text_color}; line-height: 1.4;"
        )  # Mejor altura de línea

        item_widget.setStyleSheet(
            f"""
            QWidget {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 8px;
                margin: 4px 0;
                padding: 4px;
            }}
            QWidget:hover {{
                border-color: {text_color};
                background-color: #FFFFFF;
            }}
        """
        )

        item_layout.addWidget(icon_label)
        item_layout.addWidget(
            message_label, 1
        )  # El mensaje toma todo el espacio disponible

        return item_widget

    def create_executive_trends_section(self):
        """Sección de tendencias rápidas con mini gráficos"""
        trends_card = UltraModernCard(padding=24)  # Aumentar padding
        trends_card.setMinimumHeight(200)  # Altura mínima en lugar de máxima
        trends_card.setMaximumHeight(240)  # Altura máxima más generosa

        # Título de la sección con mejor espaciado
        title_layout = QHBoxLayout()
        title_layout.setSpacing(8)
        title_icon = QLabel("📈")
        title_icon.setStyleSheet(ICON_STYLE_MEDIUM)

        title_label = QLabel("Tendencias Rápidas")
        title_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        title_font.setPointSize(self.theme.TYPOGRAPHY["text_lg"])
        title_font.setWeight(self.theme.TYPOGRAPHY["font_semibold"])
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {self.theme.COLORS['gray_900']};")

        title_layout.addWidget(title_icon)
        title_layout.addWidget(title_label)
        title_layout.addStretch()

        # Mini indicadores de tendencia con espaciado mejorado
        trends_grid = QGridLayout()
        trends_grid.setSpacing(16)  # Incrementar espaciado entre elementos

        # Datos de tendencias
        trend_data = [
            {"label": "Ventas 7d", "trend": "↗️", "value": "+8.5%", "color": "#10B981"},
            {"label": "Clientes", "trend": "↘️", "value": "-3.2%", "color": "#EF4444"},
            {
                "label": "Satisfacción",
                "trend": "↗️",
                "value": "+0.4",
                "color": "#10B981",
            },
            {"label": "Eficiencia", "trend": "↗️", "value": "+12%", "color": "#10B981"},
        ]

        for i, trend in enumerate(trend_data):
            trend_item = self.create_mini_trend_item(trend)
            trends_grid.addWidget(trend_item, 0, i)

        trends_card.main_layout.addLayout(title_layout)
        trends_card.main_layout.addSpacing(16)  # Espaciado entre título y contenido
        trends_card.main_layout.addLayout(trends_grid)

        return trends_card

    def create_mini_trend_item(self, trend_data):
        """Crear mini indicador de tendencia"""
        item_widget = QWidget()
        item_layout = QVBoxLayout(item_widget)
        item_layout.setContentsMargins(8, 6, 8, 6)
        item_layout.setSpacing(2)

        # Etiqueta
        label = QLabel(trend_data["label"])
        label_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        label_font.setPointSize(10)
        label.setFont(label_font)
        label.setStyleSheet(f"color: {self.theme.COLORS['gray_600']};")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Trend y valor
        trend_layout = QHBoxLayout()
        trend_icon = QLabel(trend_data["trend"])
        trend_icon.setStyleSheet("font-size: 14px;")

        value_label = QLabel(trend_data["value"])
        value_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        value_font.setPointSize(12)
        value_font.setWeight(600)
        value_label.setFont(value_font)
        value_label.setStyleSheet(f"color: {trend_data['color']};")

        trend_layout.addWidget(trend_icon)
        trend_layout.addWidget(value_label)
        trend_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        item_layout.addWidget(label)
        item_layout.addLayout(trend_layout)

        item_widget.setStyleSheet(
            f"""
            QWidget {{
                background-color: {self.theme.COLORS['gray_50']};
                border: 1px solid {self.theme.COLORS['gray_200']};
                border-radius: 6px;
            }}
        """
        )

        return item_widget

    def create_main_comparison_cards(self):
        """Crear cards principales de comparación"""
        comparison_card = UltraModernCard(padding=20)

        # Título de la sección
        title_layout = QHBoxLayout()
        title_label = QLabel("📊 Comparación Principal")
        title_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        title_font.setPointSize(self.theme.TYPOGRAPHY["text_lg"])
        title_font.setWeight(self.theme.TYPOGRAPHY["font_semibold"])
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {self.theme.COLORS['gray_900']};")

        title_layout.addWidget(title_label)
        title_layout.addStretch()

        # Grid de comparaciones principales (2x2)
        comparison_grid = QGridLayout()
        comparison_grid.setSpacing(16)

        # Datos comparativos de ejemplo
        comparison_data = [
            {
                "title": "Ventas",
                "current": "€1,847",
                "previous": "€1,648",
                "change": "+12.1%",
                "trend": "up",
                "icon": "💰",
            },
            {
                "title": "Clientes",
                "current": "127",
                "previous": "138",
                "change": "-8.0%",
                "trend": "down",
                "icon": "👥",
            },
            {
                "title": "Ticket Medio",
                "current": "€14.5",
                "previous": "€11.9",
                "change": "+21.8%",
                "trend": "up",
                "icon": "🧾",
            },
            {
                "title": "Satisfacción",
                "current": "4.6★",
                "previous": "4.3★",
                "change": "+6.9%",
                "trend": "up",
                "icon": "⭐",
            },
        ]

        # Crear cards comparativas
        for i, data in enumerate(comparison_data):
            row = i // 2
            col = i % 2
            comparison_item = self.create_comparison_card(data)
            comparison_grid.addWidget(comparison_item, row, col)

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.addLayout(title_layout)
        main_layout.addSpacing(12)
        main_layout.addLayout(comparison_grid)

        comparison_card.main_layout.addLayout(main_layout)
        return comparison_card

    def create_comparison_card(self, data):
        """Crear card individual de comparación"""
        card = UltraModernCard(padding=16)
        card.setMinimumHeight(120)
        card.setMaximumHeight(140)

        # Determinar colores según trend
        if data["trend"] == "up":
            trend_color = self.theme.COLORS["green_600"]
            trend_bg = self.theme.COLORS["green_50"]
            border_color = self.theme.COLORS["green_200"]
        else:
            trend_color = self.theme.COLORS["red_600"]
            trend_bg = self.theme.COLORS["red_50"]
            border_color = self.theme.COLORS["red_200"]

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        # Header con icono y título
        header_layout = QHBoxLayout()

        icon_label = QLabel(data["icon"])
        icon_label.setStyleSheet(ICON_STYLE_MEDIUM)

        title_label = QLabel(data["title"])
        title_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        title_font.setPointSize(self.theme.TYPOGRAPHY["text_sm"])
        title_font.setWeight(self.theme.TYPOGRAPHY["font_medium"])
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {self.theme.COLORS['gray_700']};")

        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        # Comparación de valores
        values_layout = QHBoxLayout()

        # Valor actual
        current_layout = QVBoxLayout()
        current_label = QLabel("Actual")
        current_label.setStyleSheet(
            f"color: {self.theme.COLORS['gray_500']}; font-size: 10px;"
        )
        current_value = QLabel(data["current"])
        current_value.setStyleSheet(
            f"color: {self.theme.COLORS['gray_900']}; font-size: 18px; font-weight: bold;"
        )
        current_layout.addWidget(current_label)
        current_layout.addWidget(current_value)

        # Separador visual
        separator = QLabel("vs")
        separator.setStyleSheet(
            f"color: {self.theme.COLORS['gray_400']}; font-size: 12px; font-weight: 500;"
        )
        separator.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Valor anterior
        previous_layout = QVBoxLayout()
        previous_label = QLabel("Anterior")
        previous_label.setStyleSheet(
            f"color: {self.theme.COLORS['gray_500']}; font-size: 10px;"
        )
        previous_value = QLabel(data["previous"])
        previous_value.setStyleSheet(
            f"color: {self.theme.COLORS['gray_600']}; font-size: 16px; font-weight: 500;"
        )
        previous_layout.addWidget(previous_label)
        previous_layout.addWidget(previous_value)

        values_layout.addLayout(current_layout)
        values_layout.addWidget(separator)
        values_layout.addLayout(previous_layout)
        values_layout.addStretch()

        # Badge de cambio
        change_label = QLabel(data["change"])
        change_label.setStyleSheet(
            f"""
            background: {trend_bg};
            color: {trend_color};
            border: 1px solid {border_color};
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
        """
        )
        change_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Ensamblar layout
        layout.addLayout(header_layout)
        layout.addLayout(values_layout)
        layout.addWidget(change_label)
        layout.addStretch()

        card.main_layout.addLayout(layout)
        return card

    def create_trends_analysis_section(self):
        """Crear sección de análisis de tendencias"""
        trends_card = UltraModernCard(padding=20)

        # Título de la sección
        title_layout = QHBoxLayout()
        title_label = QLabel("📈 Análisis de Tendencias")
        title_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        title_font.setPointSize(self.theme.TYPOGRAPHY["text_lg"])
        title_font.setWeight(self.theme.TYPOGRAPHY["font_semibold"])
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {self.theme.COLORS['gray_900']};")

        title_layout.addWidget(title_label)
        title_layout.addStretch()

        # Placeholder para gráficos de tendencias
        trends_content = QVBoxLayout()

        # Información de tendencias
        trends_info = QLabel(
            """
        📊 Gráfico de ventas últimos 30 días (Próximamente)
        📈 Evolución de clientes mensual (En desarrollo)
        🎯 Cumplimiento de objetivos trimestrales (Planificado)
        📋 Dashboard de KPIs comparativos (Futuro)
        """
        )
        trends_info.setStyleSheet(
            f"""
            color: {self.theme.COLORS['gray_600']};
            background: {self.theme.COLORS['gray_50']};
            padding: 20px;
            border-radius: 8px;
            border: 1px dashed {self.theme.COLORS['gray_300']};
            font-size: 14px;
            line-height: 1.6;
        """
        )

        trends_content.addWidget(trends_info)

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.addLayout(title_layout)
        main_layout.addSpacing(12)
        main_layout.addLayout(trends_content)

        trends_card.main_layout.addLayout(main_layout)
        return trends_card

    def create_insights_section(self):
        """Crear sección de insights y recomendaciones"""
        insights_card = UltraModernCard(padding=20)

        # Título de la sección
        title_layout = QHBoxLayout()
        title_label = QLabel("💡 Insights y Recomendaciones")
        title_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        title_font.setPointSize(self.theme.TYPOGRAPHY["text_lg"])
        title_font.setWeight(self.theme.TYPOGRAPHY["font_semibold"])
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {self.theme.COLORS['gray_900']};")

        title_layout.addWidget(title_label)
        title_layout.addStretch()

        # Lista de insights
        insights_layout = QVBoxLayout()
        insights_layout.setSpacing(12)

        # Insights basados en la comparación
        insights = [
            {
                "type": "positive",
                "title": "Crecimiento en Ticket Medio",
                "description": "El ticket medio ha aumentado un 21.8%, sugiriendo mejor upselling o productos de mayor valor.",
                "action": "Continuar estrategia de productos premium",
                "icon": "✅",
            },
            {
                "type": "warning",
                "title": "Descenso en Base de Clientes",
                "description": "Reducción del 8% en clientes activos. Posible impacto estacional o competencia.",
                "action": "Revisar estrategias de retención y captación",
                "icon": "⚠️",
            },
            {
                "type": "info",
                "title": "Mejora en Satisfacción",
                "description": "Incremento del 6.9% en satisfacción del cliente. Las mejoras implementadas están funcionando.",
                "action": "Documentar y replicar mejores prácticas",
                "icon": "📋",
            },
        ]

        for insight in insights:
            insight_item = self.create_insight_item(insight)
            insights_layout.addWidget(insight_item)

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.addLayout(title_layout)
        main_layout.addSpacing(12)
        main_layout.addLayout(insights_layout)

        insights_card.main_layout.addLayout(main_layout)
        return insights_card

    def create_insight_item(self, insight_data):
        """Crear item individual de insight"""
        item_widget = QWidget()
        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(16, 12, 16, 12)
        item_layout.setSpacing(12)

        # Determinar colores según tipo
        if insight_data["type"] == "positive":
            bg_color = "#F0FDF4"
            border_color = "#BBF7D0"
            icon_color = "#16A34A"
        elif insight_data["type"] == "warning":
            bg_color = "#FFFBEB"
            border_color = "#FED7AA"
            icon_color = "#D97706"
        else:
            bg_color = "#EFF6FF"
            border_color = "#BFDBFE"
            icon_color = "#2563EB"

        # Icono
        icon_label = QLabel(insight_data["icon"])
        icon_label.setStyleSheet(f"font-size: 16px; color: {icon_color};")

        # Contenido del insight
        content_layout = QVBoxLayout()
        content_layout.setSpacing(4)

        # Título
        title_label = QLabel(insight_data["title"])
        title_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        title_font.setPointSize(self.theme.TYPOGRAPHY["text_sm"])
        title_font.setWeight(self.theme.TYPOGRAPHY["font_semibold"])
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {self.theme.COLORS['gray_900']};")

        # Descripción
        desc_label = QLabel(insight_data["description"])
        desc_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        desc_font.setPointSize(self.theme.TYPOGRAPHY["text_xs"])
        desc_label.setFont(desc_font)
        desc_label.setStyleSheet(f"color: {self.theme.COLORS['gray_600']};")
        desc_label.setWordWrap(True)

        # Acción recomendada
        action_label = QLabel(f"💡 {insight_data['action']}")
        action_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        action_font.setPointSize(self.theme.TYPOGRAPHY["text_xs"])
        action_font.setWeight(self.theme.TYPOGRAPHY["font_medium"])
        action_label.setFont(action_font)
        action_label.setStyleSheet(f"color: {icon_color};")

        content_layout.addWidget(title_label)
        content_layout.addWidget(desc_label)
        content_layout.addWidget(action_label)

        # Ensamblar layout
        item_layout.addWidget(icon_label)
        item_layout.addLayout(content_layout)

        # Styling del item
        item_widget.setStyleSheet(
            f"""
            QWidget {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 8px;
                margin: 2px 0;
            }}
        """
        )

        return item_widget

    def create_detailed_category_section(self, category_data):
        """Crear sección de categoría para la vista detallada"""
        section_card = UltraModernCard(padding=20)

        # Header de la categoría
        header_layout = QHBoxLayout()

        # Título e ícono de la categoría
        title_label = QLabel(category_data["title"])
        title_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        title_font.setPointSize(self.theme.TYPOGRAPHY["text_lg"])
        title_font.setWeight(self.theme.TYPOGRAPHY["font_semibold"])
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {self.theme.COLORS['gray_900']};")

        # Descripción de la categoría
        desc_label = QLabel(category_data["description"])
        desc_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        desc_font.setPointSize(self.theme.TYPOGRAPHY["text_sm"])
        desc_label.setFont(desc_font)
        desc_label.setStyleSheet(f"color: {self.theme.COLORS['gray_600']};")

        # Layout vertical para título y descripción
        title_layout = QVBoxLayout()
        title_layout.addWidget(title_label)
        title_layout.addWidget(desc_label)
        title_layout.setSpacing(4)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()

        # Grid de métricas de la categoría (2 columnas para más espacio)
        metrics_grid = QGridLayout()
        metrics_grid.setSpacing(16)

        for i, metric in enumerate(category_data["metrics"]):
            row = i // 2  # 2 columnas
            col = i % 2
            metric_card = self.create_detailed_metric_card(metric)
            metrics_grid.addWidget(metric_card, row, col)

        # Layout principal de la sección
        main_layout = QVBoxLayout()
        main_layout.addLayout(header_layout)
        main_layout.addSpacing(16)
        main_layout.addLayout(metrics_grid)

        section_card.main_layout.addLayout(main_layout)
        return section_card

    def create_detailed_metric_card(self, metric_data):
        """Crear tarjeta de métrica individual para vista detallada"""
        card = UltraModernCard(padding=16)
        card.setMinimumHeight(100)
        card.setMaximumHeight(120)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        # Icono de la métrica
        icon_label = QLabel(metric_data["icon"])
        icon_label.setStyleSheet("font-size: 24px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setFixedSize(40, 40)

        # Información de la métrica
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)

        # Título
        title_label = QLabel(metric_data["title"])
        title_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        title_font.setPointSize(self.theme.TYPOGRAPHY["text_sm"])
        title_font.setWeight(self.theme.TYPOGRAPHY["font_medium"])
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {self.theme.COLORS['gray_700']};")

        # Valor principal
        value_label = QLabel(metric_data["value"])
        value_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        value_font.setPointSize(self.theme.TYPOGRAPHY["text_xl"])
        value_font.setWeight(self.theme.TYPOGRAPHY["font_bold"])
        value_label.setFont(value_font)
        value_label.setStyleSheet(f"color: {self.theme.COLORS['gray_900']};")

        # Período
        period_label = QLabel(metric_data["period"])
        period_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        period_font.setPointSize(self.theme.TYPOGRAPHY["text_xs"])
        period_label.setFont(period_font)
        period_label.setStyleSheet(f"color: {self.theme.COLORS['gray_500']};")

        info_layout.addWidget(title_label)
        info_layout.addWidget(value_label)
        info_layout.addWidget(period_label)

        # Trend
        trend_layout = QVBoxLayout()
        trend_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Determinar color del trend
        if metric_data["trend"].startswith("+"):
            trend_color = self.theme.COLORS["green_600"]
            trend_bg = self.theme.COLORS["green_100"]
        elif metric_data["trend"].startswith("-"):
            trend_color = self.theme.COLORS["red_600"]
            trend_bg = self.theme.COLORS["red_100"]
        else:
            trend_color = self.theme.COLORS["gray_600"]
            trend_bg = self.theme.COLORS["gray_100"]

        trend_label = QLabel(metric_data["trend"])
        trend_font = QFont(self.theme.TYPOGRAPHY["font_family"])
        trend_font.setPointSize(self.theme.TYPOGRAPHY["text_sm"])
        trend_font.setWeight(self.theme.TYPOGRAPHY["font_semibold"])
        trend_label.setFont(trend_font)
        trend_label.setStyleSheet(
            f"""
            color: {trend_color};
            background: {trend_bg};
            padding: 4px 8px;
            border-radius: 4px;
        """
        )

        trend_layout.addWidget(trend_label)

        # Ensamblar layout
        layout.addWidget(icon_label)
        layout.addLayout(info_layout)
        layout.addStretch()
        layout.addLayout(trend_layout)

        card.main_layout.addLayout(layout)
        return card

    def create_real_data_kpis(self, kpis_grid):
        """Crear KPIs usando SOLO datos reales y componentes especializados de hostelería"""
        logger.info("🔄 Creando KPIs ejecutivos con DATOS REALES únicamente")

        # Obtener datos reales del RealDataManager
        self.data_manager.fetch_all_real_data()
        real_data = getattr(self.data_manager, "_data_cache", {})
        logger.info(f"📊 Datos reales disponibles: {list(real_data.keys())}")

        # Mapeo de métricas ejecutivas a tipos de HospitalityMetricCard
        executive_metrics = [
            {
                "key": "ventas_diarias",
                "metric_type": "ventas_diarias",
                "row": 0,
                "col": 0,
            },
            {"key": "margen_bruto", "metric_type": "margen_bruto", "row": 0, "col": 1},
            {
                "key": "mesas_ocupadas",
                "metric_type": "mesas_ocupadas",
                "row": 0,
                "col": 2,
            },
            {
                "key": "satisfaccion_cliente",
                "metric_type": "satisfaccion",
                "row": 1,
                "col": 0,
            },
            {
                "key": "comandas_activas",
                "metric_type": "comandas_activas",
                "row": 1,
                "col": 1,
            },
            {
                "key": "ticket_promedio",
                "metric_type": "ticket_promedio",
                "row": 1,
                "col": 2,
            },
        ]

        # Crear tarjetas especializadas usando datos reales
        for metric_config in executive_metrics:
            key = metric_config["key"]
            metric_type = metric_config["metric_type"]

            # Obtener datos reales para esta métrica
            metric_data = real_data.get(key, {})
            value = metric_data.get("value", 0)
            trend = metric_data.get("trend", 0)

            # Formatear trend como string
            trend_str = f"{'+' if trend >= 0 else ''}{trend:.1f}%"

            logger.info(f"📊 Creando KPI {key}: value={value}, trend={trend_str}")

            # Crear tarjeta especializada
            kpi_card = HospitalityMetricCard(
                metric_type=metric_type, value=str(value), trend=trend_str
            )

            # Configurar tamaño para vista ejecutiva
            kpi_card.setMinimumSize(180, 120)
            kpi_card.setMaximumSize(280, 150)

            # Agregar al grid
            kpis_grid.addWidget(kpi_card, metric_config["row"], metric_config["col"])

            logger.info(
                f"✅ KPI {key} agregado al grid en posición ({metric_config['row']}, {metric_config['col']})"
            )
        logger.info("✅ Todos los KPIs ejecutivos creados con datos reales")
