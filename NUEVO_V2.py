import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit.components.v1 import html

# ================================
# ✅ CONFIGURACIÓN PAGINA
# ================================
st.set_page_config(
    page_title="Seguimiento O&M Movil",
    layout="wide",
)

st.markdown("""   
<style>
.block-container {
    padding-top: 1rem !important;
}
</style>
""", unsafe_allow_html=True)

# ================================
# ✅ CONTROL DE PANTALLAS_NEW
# ================================
if "vista" not in st.session_state:
    st.session_state.vista = "dashboard"


st.markdown("<br><br>", unsafe_allow_html=True)

# ================================
# ✅ BOTONES NAVEGACION_NEW
# ===============================
col_nav1, col_nav2, col_nav3, col_nav4 = st.columns(4)

with col_nav1:
    if st.button("📊 Dashboard", use_container_width=True):
        st.session_state.vista = "dashboard"

with col_nav2:
    if st.button("📋 Seguimiento", use_container_width=True):
        st.session_state.vista = "seguimiento"

with col_nav3:
    if st.button("📋 Recepción", use_container_width=True):
        st.session_state.vista = "Recepcion"

with col_nav4:
    if st.button("✅ Preventivos", use_container_width=True):
        st.session_state.vista = "Preventivos"


# ================================
# ✅ TITULO-HEADER
# ================================
from streamlit.components.v1 import html

html("""
<div style="
    background-color:#c0392b;
    color:white;
    padding:25px 20px;
    border-radius:10px;
    display:flex;
    align-items:center;
    justify-content:center;
    gap:12px;
    margin-bottom:20px;
">
    
    <div style="font-size:28px;">📡</div>
        
    <div style="font-size:26px; font-weight:bold;">
        Reporte Fallas Activas O&M

</div>

</div>
""", height=100)
    
        
# ================================
# ✅ HORA
# ================================
from datetime import datetime

hora_actual = datetime.now().strftime("%H:%M:%S")

col1, col2 = st.columns([8, 2])   

with col1:
    st.write("")  # espacio (no muestra nada)

with col2:
    st.markdown(f"""
    <div style=" 
        background:#2c3e50;
        color:white;
        padding:8px;   
        border-radius:8px; 
        text-align:center;
        font-weight:bold;
    ">
        🕒 {hora_actual}
    </div>
    """, unsafe_allow_html=True)
    
# ================================
# ✅ LEER DATOS
# ================================
ruta = "/Users/diegoalejandromartinvivas/Desktop/INDICADORES 2026/reporte fallas diario.xlsx"
ruta_recepcion = "/Users/diegoalejandromartinvivas/Desktop/INDICADORES 2026/Recepcion.xlsx"
ruta_Preventivos = "/Users/diegoalejandromartinvivas/Desktop/INDICADORES 2026/MP_SITE.xlsx"


#==xls = pd.ExcelFile(ruta_Preventivos)
#==st.write(xls.sheet_names)



df = pd.read_excel(ruta, sheet_name="DATA MAXIMO")
        
df_seguimiento = pd.read_excel(ruta, sheet_name="SEGUIMIENTO")

df_Recepcion = pd.read_excel(ruta_recepcion, sheet_name="RI")

df_Preventivos = pd.read_excel(ruta_Preventivos, sheet_name="PREVENTIVOS")



# ================================
# ✅ FILTRO BASE
# ================================
df = df[df["FILTRO_SUMARY"] == 1] 


# ================================
# ✅ DASHBOARD
# ================================
if st.session_state.vista == "dashboard":



  # ================================
  # ✅ LISTA ZONAS
  # ================================
  zonas = ["Todas"] + sorted(df["ZONA"].dropna().unique().tolist())
    
  # ================================
  # ✅ FILA DE FILTROS
  # ================================
  col1, col2 = st.columns([2, 3])
        
  # ✅ ZONA
  with col1:
    zona_seleccionada = st.selectbox(
        "Zona",
        zonas
    )
  # ✅ FILTRAR TEMPORAL PARA RESPONSABLES
  df_filtrado_zona = df.copy()

  if zona_seleccionada != "Todas":
    df_filtrado_zona = df_filtrado_zona[df_filtrado_zona["ZONA"] == zona_seleccionada]
        
  # ================================
  # ✅ RESPONSABLE DINÁMICO
  # ================================
  responsables = ["Todos"] + sorted(df_filtrado_zona["Responsable"].dropna().unique().tolist())

  with col2:
    responsable_seleccionado = st.selectbox(
        "Responsable",
        responsables
    )

  # ================================
  # ✅ FILTRO FINAL
  # ================================
  if zona_seleccionada != "Todas":
    df = df[df["ZONA"] == zona_seleccionada]

  if responsable_seleccionado != "Todos":
    df = df[df["Responsable"] == responsable_seleccionado]
        

  #  ================================
  # ✅ CALCULO KPI
  # ================================
  total_fallas = len(df)
  acceso = len(df[df["Area"] == "ACCESO"])
  fibra = len(df[df["Area"] == "CFIBRA"])
  # ================================
  # ✅ KPI
  # ================================
  html(f"""
  <div style="display:flex; justify-content:space-between; margin:10px 0;">

    <div style="width:28%; background:#ffeaea; padding:10px; border-radius:10px;
                text-align:center; border:1px solid #ff4d4d;">
        <div style="font-size:22px;">📊</div>
        <h5 style="margin:3px;">TOTAL FALLAS</h5>
        <h2 style="color:#c0392b; margin:3px;">{total_fallas}</h2>
    </div>
     
    <div style="width:28%; background:#eaf4ff; padding:10px; border-radius:10px;
                text-align:center; border:1px solid #3498db;">
        <div style="font-size:22px;">📡</div>
        <h5 style="margin:3px;">ACCESO</h5>
        <h2 style="color:#2980b9; margin:3px;">{acceso}</h2>
    </div>

    <div style="width:28%; background:#eaffea; padding:10px; border-radius:10px;
                text-align:center; border:1px solid #27ae60;">
        <div style="font-size:22px;">🧵</div>
        <h5 style="margin:3px;">FIBRA</h5>
        <h2 style="color:#1e8449; margin:3px;">{fibra}</h2>
    </div>

  </div>
  """, height=120)

  # ================================
  # ✅ CONTROL ALERTA
  # ================================

  hay_vencidos = df["TIEMPO PARA SOLUCION"].astype(str).str.upper().eq("VENCIDO").any()
  hay_en_tiempo = ~df["TIEMPO PARA SOLUCION"].astype(str).str.upper().eq("VENCIDO").all()


    
  # ================================
  # ✅ TITULO TABLA BASE
  # ================================
  col1, col2 = st.columns([3, 7])
    
  with col1:
    st.markdown("### 📋 Detalle de Fallas")
                
  # ✅ lógica inteligente
  columna = df["TIEMPO PARA SOLUCION"].astype(str).str.upper()
        
  hay_vencidos = columna.eq("VENCIDO").any()
  todos_vencidos = columna.eq("VENCIDO").all()
    
  with col2:
    if hay_vencidos and not todos_vencidos:
        st.markdown("""
        <div style="
            background:#ffcccc;
            padding:8px;
            border-radius:6px;
            border-left:5px solid red;
            display:flex;
            align-items:center;
            height:40px;
            margin-top:10px;
        ">

     ⚠️ <strong style="margin-right:5px;">ALERTA:</strong>Existen fallas en tiempos
        </div>
        """, unsafe_allow_html=True)


  # ================================
  # ✅ CREAR TABLA BASE
  # ================================


  tabla = df[[
    "JEFATURA",
    "Responsable",
    "Orden de trabajo",
    "Ubicación",
    "Prioridad",
    "AFECTACION",
    "Incidente relacionado",
    "TIEMPO",
    "SLA CAMPO",
    "TIEMPO PARA SOLUCION",
    "HORAS EN FALLA"
  ]].copy()

  # ================================
  # ✅ RENOMBRAR COLUMNAS
  # ================================
  tabla.columns = [
    "JEFATURA",
    "RESPONSABLE",
    "ORDEN DE TRABAJO",
    "UBICACIÓN",
    "PRIORIDAD",
    "AFECTACIÓN",
    "INCIDENTE",
    "ANTIGÜEDAD",
    "SLA CAMPO",
    "TIEMPO SOLUCIÓN",
    "HORAS FALLA"
  ]

  # ================================
  # ✅ FUNCIONES COLORES
  # ================================
  def color_prioridad(valor):
    if valor == "Alto":
        return "background-color:red; color:white;"
    elif valor == "Medio":
        return "background-color:yellow;"
    elif valor == "Bajo":
        return "background-color:green; color:white;"
    return ""
    
  def color_antiguedad(valor):
    if "> A 7 DIAS" in str(valor):
        return "background-color:red; color:white;"
    elif "> 3 DIAS" in str(valor):
        return "background-color:orange;"
    elif "> 2 DIAS" in str(valor):
        return "background-color:yellow;"
    elif "> 1 DIA" in str(valor):
        return "background-color:#c6e48b;"  # verde claro
    elif "<= 1 DIA" in str(valor):
        return "background-color:green; color:white;"
    return ""   
    
  def color_tiempo_solucion(valor):
    if str(valor).upper() == "VENCIDO":
        return "background-color:red; color:white;"
    return ""   
    
  def color_horas_falla(valor, sla):
    try:
        if valor > sla:
            return "background-color:red; color:white;"
        elif valor >= sla - 1:
            return "background-color:yellow;"
        else:
            return "background-color:green; color:white;"
    except:
        return ""
        
  def sombra_fila(row):
    estilos = [""] * len(row)
    
    valor = str(row["TIEMPO SOLUCIÓN"])

    if valor.upper() == "VENCIDO":
        fondo = "background-color:#fdecea;"  # rojo suave
    else:
        fondo = "background-color:#eafaf1;"  # verde claro
    
    # ✅ aplicar fondo SIN borrar lo demás
    estilos = [fondo] * len(row) 
        
    return estilos

  # ================================
  # ✅ FORMATO DE NUMEROS
  # ================================
  tabla["HORAS FALLA"] = pd.to_numeric(tabla["HORAS FALLA"], errors="coerce").round(2)
            
  # ================================
  # ✅ FORMATEO INTELIGENTE
  # ================================
  def format_tiempo(valor):
    try:
        return f"{float(valor):.2f}"
    except:
        return valor  # mantiene "VENCIDO"
    
  # ================================
  # ✅ APLICAR FORMATO
  # ================================
  tabla["TIEMPO SOLUCIÓN"] = tabla["TIEMPO SOLUCIÓN"].apply(format_tiempo)
        

  # ================================
  # ✅ APLICAR ESTILOS A TABLA
  # ================================
        
  styled_tabla = (
    tabla.style
    .apply(sombra_fila, axis=1)  # 🔥 PRIMERO fondo base
    .map(color_prioridad, subset=["PRIORIDAD"])
    .map(color_antiguedad, subset=["ANTIGÜEDAD"])
    .map(color_tiempo_solucion, subset=["TIEMPO SOLUCIÓN"])
    .apply(
        lambda row: [
            color_horas_falla(row["HORAS FALLA"], row["SLA CAMPO"])
            if col == "HORAS FALLA" else ""
            for col in tabla.columns
        ],
        axis=1
    )
  )


  # ================================
  # ✅ MOSTRAR TABLA (PRO)
  # ================================
        
  html_tabla = styled_tabla.to_html()

  CUSTOM_CSS = """
  <style>
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }

 }
  /* ✅ ENCABEZADO DE TABLA */
  thead th {
    background-color:#2c3e50 !important;
    color: white !important;
    font-weight: bold;
    text-align: center;
    padding: 10px;
  }
    
    
        
  /* ✅ Orden de trabajo */
  td:nth-child(3), th:nth-child(3) {
    text-align: center;
    width: 120px;
  }
     
  /* ✅ SLA CAMPO */
  td:nth-child(9), th:nth-child(9) {
    text-align: center;
    width: 80px;
  }

  /* ✅ Tiempo solución */
  td:nth-child(10), th:nth-child(10) {
    text-align: center;
    width: 120px;
  }

  /* ✅ Horas falla */
  td:nth-child(11), th:nth-child(11) {
    text-align: center;
    width: 120px;
  }
  </style>
  """
    
  st.markdown(CUSTOM_CSS + html_tabla, unsafe_allow_html=True)
  # ================================
  # ✅ FILTRO POR ZONA
  # ================================
  if zona_seleccionada != "Todas":
    df = df[df["ZONA"] == zona_seleccionada]

      # ================================
  # ✅ GRAFICO POR ZONA
  # ================================
  zona_df = df["ZONA"].value_counts().reset_index()
  zona_df.columns = ["ZONA", "TOTAL"]
    
  fig_zona = px.bar(
    zona_df,
    x="ZONA",
    y="TOTAL",
    color="TOTAL",
    title="Afectación por Zona"
  )

  # ================================
  # ✅ GRAFICO PRIORIDAD
  # ================================  
  prio_df = df["Prioridad"].value_counts().reset_index()
  prio_df.columns = ["Prioridad", "TOTAL"]
 
  fig_prio = px.pie(
    prio_df,
    names="Prioridad",
    values="TOTAL",
    title="Distribución por Prioridad"
  )   

  # ================================
  # ✅ MOSTRAR GRAFICOS
  # ================================
  col3, col4 = st.columns(2)

  col3.plotly_chart(fig_zona, use_container_width=True)
  col4.plotly_chart(fig_prio, use_container_width=True)

  # ================================
  # ✅ TABLA FINAL
  # ================================ 
  st.dataframe(df, use_container_width=True)
 


# ================================
# ✅ SEGUIMIENTO
# ================================
elif st.session_state.vista == "seguimiento":
# ================================
        
    st.markdown("## 📋 Seguimiento OT")

    df_filtro = df_seguimiento.copy()

    # ----------------------------
    # ✅ FILTROS
    # ----------------------------

    zonas = ["Todas"] + sorted(df_filtro["ZONA"].dropna().unique())
    responsables = ["Todos"] + sorted(df_filtro["Responsable"].dropna().unique())
    estados = ["Todos"] + sorted(df_filtro["Estado O&M"].dropna().unique())

    col1, col2, col3 = st.columns(3)

    with col1:
        zona = st.selectbox("Zona", zonas)

    with col2:
        responsable = st.selectbox("Responsable", responsables)

    with col3:
        estado = st.selectbox("Estado O&M", estados)

    # ----------------------------
    # ✅ FILTRO APLICADO
    # ----------------------------

    if zona != "Todas":
        df_filtro = df_filtro[df_filtro["ZONA"] == zona]

    if responsable != "Todos":
        df_filtro = df_filtro[df_filtro["Responsable"] == responsable]

    if estado != "Todos":
        df_filtro = df_filtro[df_filtro["Estado O&M"] == estado]
    
    # ----------------------------
    # ✅ KPI INTELIGENTE
    # ----------------------------
    columna = df_filtro["TIEMPO PARA SOLUCION"].astype(str).str.upper()

    total = len(df_filtro)
    vencidos = columna.eq("VENCIDO").sum()
    no_cumple = columna.eq("NO CUMPLE").sum()
    si_cumple = columna.eq("SI CUMPLE").sum()

   # ✅ EN TIEMPO → SOLO NUMÉRICOS
    en_tiempo = columna.str.replace(".", "", regex=False).str.isnumeric().sum()

   # ----------------------------
   # ✅ VISUAL KPI
   # ----------------------------

    html(f"""
     <div style="display:flex; gap:10px; margin:10px 0;">

      <div style="flex:1;background:#f0f0f0;padding:10px;text-align:center;border-radius:8px;">
        <h4>📊 TOTAL OT</h4><h2>{total}</h2>
      </div>

      <div style="flex:1;background:#ffeaea;padding:10px;text-align:center;border-radius:8px;">
        <h4>🔴 VENCIDOS</h4><h2>{vencidos}</h2>
      </div>

      <div style="flex:1;background:#f8c8dc;padding:10px;text-align:center;border-radius:8px;">
        <h4>🌸 NO CUMPLE</h4><h2>{no_cumple}</h2>
      </div>

      <div style="flex:1;background:#eaffea;padding:10px;text-align:center;border-radius:8px;">
        <h4>🟢 SI CUMPLE</h4><h2>{si_cumple}</h2>
      </div>

      <div style="flex:1;background:#eaf4ff;padding:10px;text-align:center;border-radius:8px;">
        <h4>⏱️ EN TIEMPO</h4><h2>{en_tiempo}</h2>
      </div>

    </div>
    """, height=130)


    # ----------------------------
    # ✅ TABLA
    # ----------------------------

    tabla = df_filtro[[
        "JEFATURA",
        "Orden de trabajo",
        "Ubicación",
        "HORAS EN FALLA",
        "Estado O&M",
        "OBSERVACION",
        "Prioridad",
        "SLA CAMPO",
        "TIEMPO PARA SOLUCION",
        "Incidente relacionado",
        "AFECTACION",
        "TIEMPO",
        "Responsable"
    ]].copy()
    
    
    # ----------------------------
    # ✅ ORDENAMIENTO
    # ----------------------------
    col1, col2 = st.columns(2)
    with col1:
     columna = st.selectbox("Ordenar por:", tabla.columns)
    
    with col2:
     orden = st.radio("Orden:", ["Ascendente", "Descendente"], horizontal=True)

    tabla = tabla.sort_values(
     by=columna,
     ascending=(orden == "Ascendente")
    )

    # ----------------------------
    # ✅ FUNCIONES DE COLOR
    # ----------------------------

    def color_prioridad(v):
        if v == "Alto":
            return "background:red; color:white;"
        elif v == "Medio":
            return "background:yellow;"
        elif v == "Bajo":
            return "background:green; color:white;"
        return ""

    
    def color_estado(v):
        if v == "SOLUCIONADO":
         # Verde tipo "OK"
         return "background:green; color:white;"
        elif v == "OT CANCELADA":
         # Gris
         return "background:gray; color:white;"
        elif v == "FALLA FIBRA PLANTA EXTERNA":
        # Rosado
         return "background:pink; color:black;"
        return ""  # Otros estados sin color

    def color_afectacion(v):
        if str(v).upper() == "TOTAL":
            return "background:red; color:white;"
        return ""

    def color_tiempo(v):
        if str(v).upper() == "VENCIDO":
            return "background:red; color:white;"
        return ""

    def color_horas_falla(valor, sla):
        try:
            if valor > sla:
                return "background:red; color:white;"
            elif valor >= sla - 1:
                return "background:yellow;"
            else:
                return "background:green; color:white;"
        except:
            return ""
    
    
    def color_tiempo_solucion(valor):
        v = str(valor).upper()

        if v == "VENCIDO":
          return "background-color:red; color:white;"
        elif v == "NO CUMPLE":
          return "background-color:#f8c8dc; color:red;"  # rosado
        elif v == "SI CUMPLE":
          return "background-color:green; color:white;"
        else:
          return ""  # valores numéricos se dejan igual


    def sombra_fila(row):
        if str(row["TIEMPO PARA SOLUCION"]).upper() == "VENCIDO":
            return ["background-color:#fdecea"] * len(row)
        else:
            return ["background-color:#eafaf1"] * len(row)

    # ----------------------------
    # ✅ FORMATO
    # ----------------------------

    tabla["HORAS EN FALLA"] = pd.to_numeric(tabla["HORAS EN FALLA"], errors="coerce")

    # ----------------------------
    # ✅ APLICAR ESTILOS
    # ----------------------------

    styled = (
        tabla.style
        .apply(sombra_fila, axis=1)
        .map(color_estado, subset=["Estado O&M"])
        .map(color_prioridad, subset=["Prioridad"])
        .map(color_afectacion, subset=["AFECTACION"])
        .map(color_tiempo_solucion, subset=["TIEMPO PARA SOLUCION"])
        .apply(
            lambda row: [
                color_horas_falla(row["HORAS EN FALLA"], row["SLA CAMPO"])
                if col == "HORAS EN FALLA" else ""
                for col in tabla.columns
            ],
           axis=1
        )
    )

    # ----------------------------
    # ✅ tabla re- PRO
    # ----------------------------
    
    css = """
    <style>
    table {
     width:100%;
     font-size:13px;
     border-collapse: collapse;
    }

    thead th {
     background:#2c3e50;
     color:white;
     text-align:center;
     padding:10px;
    }

    td {
     padding:8px;
     text-align:center;
     white-space: normal !important;
     word-wrap: break-word;
     max-width: 400px;
    }

    td:nth-child(6) {  /* OBSERVACION */
     text-align:left;
     max-width: 500px;
    }
    .scroll-table {
    max-height: 600px;
    overflow-y: auto;
    }

    /* Scroll bonito */
    .scroll-table::-webkit-scrollbar {
      width: 6px;
    }
    .scroll-table::-webkit-scrollbar-thumb {
     background-color: #888;
     border-radius: 4px;
    }
    .scroll-table::-webkit-scrollbar-thumb:hover {
     background-color: #555;
    }

    </style>
    """
    html_tabla = styled.to_html()

    html(
     f"""
     {css}
     <div class="scroll-table">
        {html_tabla}
     </div>
     """,
     height=660
    )

    
    # ✅== DESCARGAR TABLA==
    
    from io import BytesIO

    output = BytesIO()

    # ✅ escribir Excel en memoria
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
     tabla.to_excel(writer, index=False, sheet_name="Seguimiento")

    # ✅ obtener archivo
    excel_data = output.getvalue()

    # ✅ botón descarga
    st.download_button(
     label="📥 Descargar tabla en Excel",
     data=excel_data,
     file_name="reporte_seguimiento.xlsx",
     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )



    # ==== GRAFICOS SEGUIMIENTO======
    # ================================

    # ✅ 1. OT por Zona
    graf_zona = (
    df_filtro.groupby("ZONA")["Orden de trabajo"]
    .count()
    .reset_index()
    )

    fig_zona = px.bar(
    graf_zona,
    x="ZONA",
    y="Orden de trabajo",
    title="📊 Orden de trabajo por Zona",
    color="Orden de trabajo",
    )
    
    fig_zona.update_layout(
    showlegend=False,
    xaxis_title="Zona",
    yaxis_title="Total OT"
    )




    # ================================
    # ✅ GRAFICO DISTRIBUCIÓN TIEMPO (HORIZONTAL)
    # ================================


    # ✅ agrupar datos
    graf_tiempo = df_filtro["TIEMPO"].value_counts().reset_index()
    graf_tiempo.columns = ["TIEMPO", "TOTAL"]

    # ✅ ordenar de mayor a menor
    graf_tiempo = graf_tiempo.sort_values(by="TOTAL", ascending=True)

    # 🎨 colores personalizados (tipo dashboard pro)
    color_tiempo_map = {
    "<= 1 DIA": "#3498db",                  # azul
    "> 1 DIA Y <= A 2 DIAS": "#f39c12",     # naranja
    "> A 7 DIAS": "#e74c3c"                 # rojo
    }

    # ✅ gráfico horizontal
    fig_tiempo = px.bar(
    graf_tiempo,
    y="TIEMPO",
    x="TOTAL",
    orientation="h",
    text="TOTAL",
    title="⏱️ Distribución por Tiempo",
    color="TIEMPO",
    color_discrete_map=color_tiempo_map
    )

    # ✅ estilo visual (MUY PRO)
    fig_tiempo.update_layout(
    showlegend=False,
    xaxis_title="Total OT",
    yaxis_title="",
    )

    fig_tiempo.update_traces(textposition="outside")


    # ✅ GRAFICO ESTADO O&M (HORIZONTAL PRO)
    # ================================

    # ✅ agrupar datos
    graf_estado = df_filtro["Estado O&M"].value_counts().reset_index()
    graf_estado.columns = ["Estado O&M", "TOTAL"]

    # ✅ ordenar (más grandes abajo → visual mejor)
    graf_estado = graf_estado.sort_values(by="TOTAL", ascending=True)

    # 🎨 colores personalizados
    
    
    # ✅ función de color (CORRECTA)
    def get_color(estado):
     if estado == "SOLUCIONADO":
        return "#27ae60"   # verde
     elif estado == "OT CANCELADA":
        return "#7f8c8d"   # gris
     elif estado == "FALLA FIBRA PLANTA EXTERNA":
        return "#e67e22"   # naranja
     else:
        return "#3498db"   # azul

    graf_estado["COLOR"] = graf_estado["Estado O&M"].apply(get_color)

    fig_estado = px.bar(
    graf_estado,
    y="Estado O&M",
    x="TOTAL",
    orientation="h",
    text="TOTAL",
    title="📡 Estado O&M"
    )

    fig_estado.update_traces(
    marker_color=graf_estado["COLOR"],
    textposition="outside"
    )

    fig_estado.update_layout(
    showlegend=False,
    xaxis_title="Total OT",
    yaxis_title=""
    )
    # ----------------------------
    # ✅ MOSTRAR LOS 3 EN UNA FILA
    # ----------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
     st.plotly_chart(fig_zona, use_container_width=True)

    with col2:
     st.plotly_chart(fig_tiempo, use_container_width=True)

    with col3:
     st.plotly_chart(fig_estado, use_container_width=True)

# ================================
# ✅ recepcion infraestructura
# ================================
elif st.session_state.vista == "Recepcion":
  
  #====filtro OTRAS AREAS======
  df_Recepcion = df_Recepcion[
    df_Recepcion["ESTADO_SO"] != "Otras Areas"
  ].copy()
  
  #✅ FECHA ACTUALIZACIÓN
  
  df_Recepcion["FECHA ACTUALIZACION"] = pd.to_datetime(df_Recepcion["FECHA ACTUALIZACION"], errors="coerce")

  fecha_max = df_Recepcion["FECHA ACTUALIZACION"].max()
  fecha_texto = fecha_max.strftime("%d/%m/%Y %I:%M:%S %p")
  
  # ✅ HEADER
  st.markdown(
    f"""
    <div style="
        display:flex;
        align-items:center;
        justify-content:space-between;
        font-size:28px;
        font-weight:600;
    ">
        <div>📝 Recepción</div>
        <div style="font-size:16px; font-weight:normal;">
            Fecha Actualización: {fecha_texto}
        </div>
    </div>
    """,
    unsafe_allow_html=True
  )  
  

  # ================================
  # ✅ FILTROS
  # ================================ 
  df_base = df_Recepcion.copy()
  
  df_base["Fecha_Estado"] = pd.to_datetime(
    df_base["Fecha_Estado"], errors="coerce"
  )

  df_base["MES_AÑO"] = df_base["Fecha_Estado"].dt.strftime("%m/%Y")

  
  col0, col1, col2, col3 = st.columns(4)
  
  
  # -------- PASO 0: FECHA ----------
  fechas = ["Todas"] + sorted(df_base["MES_AÑO"].dropna().unique())

  with col0:
    fecha = st.selectbox("📅 Fecha", fechas)

  df_temp = df_base.copy()

  if fecha != "Todas":
    df_temp = df_temp[df_temp["MES_AÑO"] == fecha]



  # -------- PASO 1: ZONA ----------
  zonas = ["Todas"] + sorted(df_temp["MACROZONA"].dropna().unique())

  with col1:
    zona = st.selectbox("MACROZONA", zonas)

  if zona != "Todas":
    df_temp = df_temp[df_temp["MACROZONA"] == zona]


  # -------- PASO 2: SITE OWNER ----------
  responsables = ["Todos"] + sorted(df_temp["SITE OWNER"].dropna().unique())

  with col2:
    responsable = st.selectbox("SITE OWNER", responsables)

  if responsable != "Todos":
    df_temp = df_temp[df_temp["SITE OWNER"] == responsable]


  # -------- PASO 3: ESTADO ----------
  estados = ["Todos"] + sorted(df_temp["ESTADO_SO"].dropna().unique())

  with col3:
    estado = st.selectbox("ESTADO_SO", estados)

  if estado != "Todos":
    df_temp = df_temp[df_temp["ESTADO_SO"] == estado]


  # ✅ RESULTADO FINAL
  df_filtro = df_temp.copy()
  
   
  # ================================ 
  # ✅ KPI RECEPCION
  # ================================
  df_kpi = df_filtro.copy()

  # ---- métricas base
  pendientes = (df_kpi["ESTADO_SO"] == "PENDIENTE").sum()
  ejecutado = (df_kpi["ESTADO_SO"] == "EJECUTADO SO").sum()

  # total
  total = len(df_kpi)

  # ---- KPI %
  if total > 0:
    ejecucion = (ejecutado / total) * 100
  else:
    ejecucion = 0

  ejecucion = round(ejecucion, 1)



  
  # ================================
  # ✅ VISUAL KPI
  # ================================
  st.markdown(f"""
   <div style="display:flex; gap:10px; margin:10px 0;">
        
    <div style="
        flex:1;
        background:#fff3cd;
        padding:3px;
        border-radius:10px;   
        text-align:center;
    ">
        <h4>🟡 Pendientes</h4>
        <h2>{pendientes}</h2>
    </div>
  
    <div style="
        flex:1;
        background:#d4edda;
        padding:3px;
        border-radius:10px;
        text-align:center;
    ">
        <h4>🟢 Ejecutado SO</h4>
        <h2>{ejecutado}</h2>
    </div>
  
    <div style="
        flex:1;
        background:#eaf4ff;
        padding:3px;
        border-radius:10px;
        text-align:center;
    ">
        <h4>📊 Ejecución %</h4>
        <h2>{ejecucion}%</h2>
    </div>
  
  </div>
  """, unsafe_allow_html=True) 

  # ----------------------------
  # ✅ TABLA RI
  # ----------------------------
  tabla_RI = df_filtro[[
    "ID",
    "Nombre_Sitio",
    "MACROZONA",
    "SITE OWNER",
    "DIAS",
    "Estado",
    "Tipo_Actividad",
    "Fecha_Estado",
    "ESTADO_SO",
    "KPI"
  ]].copy()

  df_base = df_filtro.copy()

  # ----------------------------
  # ✅ COLORES COLUMNAS
  # ----------------------------
  
  def color_dias(val):
    if pd.isna(val):
        return ""

    if val <= 2:
        return "background-color: #2ecc71; color:white;"  # verde

    # escala entre amarillo y rojo
    max_val = tabla_RI["DIAS"].max()
    intensidad = min(val / max_val, 1)

    # amarillo → rojo
    r = 255
    g = int(255 * (1 - intensidad))
    b = 0

    return f"background-color: rgb({r},{g},{b}); color:black;"
  
 
  def estilo_kpi(val):
    if val == "CUMPLE":
        return "background-color:#27ae60;color:white;border-radius:8px;text-align:center;font-weight:bold;"
    elif val == "NO CUMPLE":
        return "background-color:#e74c3c;color:white;border-radius:8px;text-align:center;font-weight:bold;"
    return ""
  
  # ----------------------------
  # ✅ MOSTRAR TABLA
  # 

  styled_RI = tabla_RI.style \
    .map(color_dias, subset=["DIAS"]) \
    .map(estilo_kpi, subset=["KPI"])

  st.dataframe(styled_RI, use_container_width=True)
  
  # ----------------------------
  # ✅ GRAFICOS
  # 
  st.markdown("### 📊 Evolución KPI")  
  
  df_graph = df_filtro.copy()
  
  
  df_graph["Fecha_Estado"] = pd.to_datetime(
     df_graph["Fecha_Estado"], errors="coerce")

  df_graph["MES"] = df_graph["Fecha_Estado"] \
        .dt.to_period("M").dt.to_timestamp()

  df_group = df_graph.groupby(["MES", "ESTADO_SO"])["ID"] \
     .count().unstack(fill_value=0).reset_index()

  df_group["TOTAL"] = df_group.sum(axis=1, numeric_only=True)

  col_ejecutado = "EJECUTADO SO"

  if col_ejecutado in df_group.columns:
     df_group["KPI"] = (df_group[col_ejecutado] / df_group["TOTAL"]) * 100
  else:
     df_group["KPI"] = 0

  import plotly.graph_objects as go

  fig = go.Figure()
  
  
  col_ejecutado = "EJECUTADO SO"

  if col_ejecutado in df_group.columns:
    ejecutado = df_group[col_ejecutado]
  else:
    ejecutado = pd.Series([0] * len(df_group))

  pendientes = df_group["TOTAL"] - ejecutado

  # Barras ejecutado
  fig.add_bar(
     x=df_group["MES"],
     y=ejecutado,
     name="Ejecutado SO",
     marker_color="#2ecc71",
     text=ejecutado,
     textposition="inside"
  )

  # Barras pendiente
  fig.add_bar(
    x=df_group["MES"],
    y=pendientes,
    name="Pendiente SO",
    marker_color="#f39c12",
    text=pendientes,
    textposition="inside"
  )

  # Línea KPI
  fig.add_scatter(
    x=df_group["MES"],
    y=df_group["KPI"],
    name="KPI Recepción",
    mode="lines+markers+text",
    yaxis="y2",
    text=df_group["KPI"].round(0).astype(str) + "%",
    textposition="top center",
    line=dict(color="#2e86de", width=3)
  )

  fig.update_layout(
   title="Ejecución y KPI Recepción",
   xaxis=dict(title="Mes"),
   yaxis=dict(title="Cantidad"),
   yaxis2=dict(
     title="%",
     overlaying="y",
     side="right",
     range=[0, 100]
      ),
     barmode="group",
     legend=dict(orientation="h")
  )
  

  

  if df_group.empty:
    st.info("ℹ️ No hay datos disponibles con los filtros seleccionados")
  else:
    st.plotly_chart(fig, use_container_width=True)
  
  
  st.markdown("### 📋 Resumen por SITE OWNER")

  df_resumen = df_filtro.copy()

  # ================================
  # ✅ AGRUPAR POR SITE OWNER
  # ================================
  df_summary = df_resumen.groupby(["SITE OWNER", "ESTADO_SO"])["ID"] \
    .count().unstack(fill_value=0)

  # ================================
  # ✅ ASEGURAR COLUMNAS
  # ================================
  col_ejecutado = "EJECUTADO SO"
  col_pendiente = "PENDIENTE"

  if col_ejecutado not in df_summary.columns:
    df_summary[col_ejecutado] = 0

  if col_pendiente not in df_summary.columns:
    df_summary[col_pendiente] = 0

  # ================================ 
  # ✅ RENOMBRAR
  # ================================
  df_summary = df_summary.rename(columns={
    col_ejecutado: "# EJECUTADO SO",
    col_pendiente: "# PENDIENTE"
  })

  # ================================
  # ✅ CALCULAR EJECUCIÓN %
  # ================================
  df_summary["TOTAL"] = df_summary["# EJECUTADO SO"] + df_summary["# PENDIENTE"]

  df_summary["EJECUCION_RI"] = (
    df_summary["# EJECUTADO SO"] / df_summary["TOTAL"]
  ) * 100

  # evitar división por 0
  df_summary["EJECUCION_RI"] = df_summary["EJECUCION_RI"].fillna(0).round(1)

  # ================================
  # ✅ LIMPIAR COLUMNAS
  # ================================
  df_summary = df_summary.reset_index()

  df_summary = df_summary[[
    "SITE OWNER",
    "# EJECUTADO SO",
    "# PENDIENTE",
    "EJECUCION_RI"
  ]]

  # ================================
  # ✅ FORMATO VISUAL KPI
  # ================================
  def color_kpi(val):
    if val >= 100:
        return "background-color:#2ecc71;color:white;font-weight:bold;"
    elif val >= 80:
        return "background-color:#f1c40f;color:black;"
    else:
        return "background-color:#e74c3c;color:white;font-weight:bold;"

  styled_summary = df_summary.style.map(color_kpi, subset=["EJECUCION_RI"])

  # ================================
  # ✅ MOSTRAR
  # ================================
  st.dataframe(styled_summary, use_container_width=True)

# ================================
# ✅ MANTENIMIENTOS PREVENTIVOS
# ================================
elif st.session_state.vista == "Preventivos":

 #=== ✅ FECHA ACTUALIZACIÓN==
    
  df_Preventivos["FECHA ACTUALIZACION"] = pd.to_datetime(df_Preventivos["FECHA ACTUALIZACION"], errors="coerce")
    
  fecha_max = df_Preventivos["FECHA ACTUALIZACION"].max()
  fecha_texto = fecha_max.strftime("%d/%m/%Y %I:%M:%S %p")
    
  # ✅ HEADER
  st.markdown(
    f"""
    <div style="
        display:flex;
        align-items:center;
        justify-content:space-between;
        font-size:28px;
        font-weight:600;
    ">
        <div>📝 Preventivos</div>
        <div style="font-size:16px; font-weight:normal;">
            Fecha Actualización: {fecha_texto}
        </div>
    </div>
    """,
    unsafe_allow_html=True
  )
  
    
  # ================================
  # ✅ FILTROS
  # ================================
  df_base = df_Preventivos.copy()
  
 
  col0, col1, col2, col3 = st.columns(4)
        
  
  # -------- PASO 0: FECHA ----------
  fechas = ["Todas"] + sorted(df_base["MES"].dropna().unique())
       
  with col0:
    fecha = st.selectbox("📅 Fecha", fechas)
  
  df_temp = df_base.copy()
    
  if fecha != "Todas":
    df_temp = df_temp[df_temp["MES"] == fecha]
    
  
  
  # -------- PASO 1: ZONA ----------
  zonas = ["Todas"] + sorted(df_temp["ZONA"].dropna().unique())
        
  with col1:
    zona = st.selectbox("ZONA", zonas)
  
  if zona != "Todas":
    df_temp = df_temp[df_temp["ZONA"] == zona]
        
  
  # -------- PASO 2: SITE OWNER ----------
  responsables = ["Todos"] + sorted(df_temp["SITE OWNER"].dropna().unique())
    
  with col2:
    responsable = st.selectbox("SITE OWNER", responsables)
        
  if responsable != "Todos":
    df_temp = df_temp[df_temp["SITE OWNER"] == responsable]

  # -------- PASO 3: ESTADO ----------
  estados = ["Todos"] + sorted(df_temp["Ejecucion"].dropna().unique())
        
  with col3:
    estado = st.selectbox("Ejecucion", estados)
        
  if estado != "Todos":
    df_temp = df_temp[df_temp["Ejecucion"] == estado]
  
    
  # ✅ RESULTADO FINAL
  df_filtro = df_temp.copy()
  
  # ----------------------------
  # ✅ TABLA PREVENTIVOS
  # ----------------------------
  tabla_MP = df_filtro[[
    "Orden de trabajo",
    "Ubicación",
    "Estado",
    "Fecha de creación",   
    "MES",
    "ZONA",
    "Ejecucion"
  ]].copy()
    
  df_base = df_filtro.copy()
  
  # ================================
  # ✅ KPI MP
  # ================================
  df_kpi_MP = df_filtro.copy()   
        
  # ---- métricas base
  MP_total = (df_kpi_MP["Orden de trabajo"]).sum()
  pendientes = (df_kpi_MP["Ejecucion"] == "PENDIENTE").sum()
  ejecutado = (df_kpi_MP["Ejecucion"] == "EJECUTADO").sum()
    
  # total
  total = len(df_kpi_MP)
        
  # ---- KPI %
  if total > 0:
    ejecucion = (ejecutado / total) * 100
  else:
    ejecucion = 0
        
  ejecucion = round(ejecucion, 1)
    
  # ================================
  # ✅ VISUAL KPI
  # ================================
  st.markdown(f"""
   <div style="display:flex; gap:10px; margin:10px 0;">
    

    <div style="
        flex:1;
        background:#eaf4ff;
        padding:3px;
        border-radius:10px;
        text-align:center;
    ">  
        <h4>📌 Total</h4>
        <h2>{total}</h2>
    </div>    


    <div style="
        flex:1;
        background:#fff3cd;
        padding:3px;
        border-radius:10px;
        text-align:center;
    ">
        <h4>⚠️️ Pendientes</h4>
        <h2>{pendientes}</h2>
    </div>
    
    <div style="
        flex:1;
        background:#d4edda;
        padding:3px;
        border-radius:10px;
        text-align:center;
    ">
        <h4>🟢 Ejecutado SO</h4>
        <h2>{ejecutado}</h2>
    </div>
  
    <div style="
        flex:1;
        background:#eaf4ff; 
        padding:3px;
        border-radius:10px;
        text-align:center;
    ">
        <h4>📊 Ejecución %</h4>
        <h2>{ejecucion}%</h2>
    </div>
  
  </div>
  """, unsafe_allow_html=True) 




  # ----------------------------
  # ✅ COLORES COLUMNAS
  # ----------------------------
  
  def Estado_color(val):
   if val == "CLOSE":
    return "background-color:#27ae60;color:white;border-radius:8px;text-align:center;font-weight:bold;"
   elif val == "CAN":
    return "color:black; text-align:center; font-weight:bold;"
   return ""
        
  def estilo_ejecucion(val):
    if val == "EJECUTADO":
        return "background-color:#27ae60;color:white;border-radius:8px;text-align:center;font-weight:bold;"
    elif val == "PENDIENTE":
        return "background-color:#e74c3c;color:white;border-radius:8px;text-align:center;font-weight:bold;"
    return ""
  
  # ----------------------------
  # ✅ MOSTRAR TABLA
  #
  
  styled_MP = tabla_MP.style \
    .map(Estado_color, subset=["Estado"]) \
    .map(estilo_ejecucion, subset=["Ejecucion"])
    
  st.dataframe(styled_MP, use_container_width=True)  
  
  # ----------------------------
  # ✅ TABLA MP SITE
  # ----------------------------
  tabla_SITE = df_filtro[[
    "SITE OWNER",
    "Ejecucion",
    "Ejecucion",
    "KPI"
  ]].copy()
  
  # ✅ AGRUPAR Y CONTAR
  df_base = df_filtro.copy()
  
  # agrupar por SITE OWNER y ESTADO
  df_group = df_base.groupby(["SITE OWNER", "Ejecucion"])["Orden de trabajo"] \
    .count().unstack(fill_value=0)
  
  # ✅ ASEGURAR LOS ESTADOS
  if "PENDIENTE" not in df_group.columns:
    df_group["PENDIENTE"] = 0

  if "EJECUTADO" not in df_group.columns:
    df_group["EJECUTADO"] = 0
  
  # ✅ RENOMBRAR Y CALCULAR KPI
  df_group = df_group.rename(columns={
    "PENDIENTE": "# PENDIENTES",
    "EJECUTADO": "# EJECUTADO"
  })

  df_group["TOTAL"] = df_group["# PENDIENTES"] + df_group["# EJECUTADO"]

  df_group["KPI"] = (
    df_group["# EJECUTADO"] / df_group["TOTAL"]
  ) * 100

  df_group["KPI"] = df_group["KPI"].fillna(0).round(1)
  
  # ✅ TABLA FINAL MP
  tabla_SITE = df_group.reset_index()[[
    "SITE OWNER",
    "# PENDIENTES",
    "# EJECUTADO",
    "KPI"
  ]]
  
  # ✅ ESTILOS COLUMNAS TABLA MP 
  
  def resaltar_fila(row):
    kpi = row["KPI"]

    if kpi >= 100:
        return ["background-color:#d4edda"] * len(row)   # verde claro
    elif kpi >= 80:
        return ["background-color:#fff3cd"] * len(row)   # amarillo
    elif kpi > 0:
        return ["background-color:#f8d7da"] * len(row)   # rosado
    else:
        return ["background-color:#f5b7b1"] * len(row)   # rojo claro

  def color_kpi(val):
    if val >= 100:
        return "background-color:#2ecc71; color:white;"   # verde
    elif val >= 80:
        return "background-color:#f1c40f; color:black;"  # amarillo
    elif val > 0:
        return "background-color:#e67e22; color:white;"  # naranja
    else:
        return "background-color:#e74c3c; color:white;"  # rojo

  # ✅ APLICAR ESTILOS TABLA MP 
  
  styled_site = tabla_SITE.style \
    .apply(resaltar_fila, axis=1) \
    .map(color_kpi, subset=["KPI"]) \
    .format({"KPI": "{:.1f}%"}) \
    .set_properties(subset=["# PENDIENTES", "# EJECUTADO", "KPI"], **{
        "text-align": "center"
    })


  # ✅ MOSTRAR  TABLA MP
  st.dataframe(styled_site, use_container_width=True)
  



  
  orden_meses = {
    "ENERO": 1,
    "FEBRERO": 2,
    "MARZO": 3,
    "ABRIL": 4,
    "MAYO": 5,
    "JUNIO": 6,
    "JULIO": 7,
    "AGOSTO": 8,
    "SEPTIEMBRE": 9,
    "OCTUBRE": 10,
    "NOVIEMBRE": 11,
    "DICIEMBRE": 12
  }
  
  df_graph = df_filtro.copy()

  df_graph["MES_ORDEN"] = df_graph["MES"].str.upper().map(orden_meses)
  df_graph = df_graph.sort_values("MES_ORDEN")

  df_group = df_graph.groupby(["MES", "Ejecucion"])["Orden de trabajo"] \
    .count().unstack(fill_value=0).reset_index()

  # ordenar después del groupby
  df_group["MES_ORDEN"] = df_group["MES"].str.upper().map(orden_meses)
  df_group = df_group.sort_values("MES_ORDEN")

  # asegurar columnas
  if "PENDIENTE" not in df_group.columns:
    df_group["PENDIENTE"] = 0
    
  if "EJECUTADO" not in df_group.columns:
    df_group["EJECUTADO"] = 0

  
  # ✅ KPI
  df_group["TOTAL"] = df_group["PENDIENTE"] + df_group["EJECUTADO"]

  df_group["KPI"] = (
    df_group["EJECUTADO"] / df_group["TOTAL"]
  ) * 100

  df_group["KPI"] = df_group["KPI"].fillna(0).round(1)


  
  # ✅ MOSTRAR GRAFICO
  #st.write(df_group.columns)

  import plotly.graph_objects as go

  fig = go.Figure()

  # ------------------ BARRAS EJECUTADO
  fig.add_bar(
    x=df_group["MES"],
    y=df_group["EJECUTADO"],
    name="Ejecutado",
    marker_color="#2ecc71",
    text=df_group["EJECUTADO"],
    textposition="outside"
  )

  # ------------------ BARRAS PENDIENTE
  fig.add_bar(
    x=df_group["MES"],
    y=df_group["PENDIENTE"],
    name="Pendiente",
    marker_color="#e74c3c",
    text=df_group["PENDIENTE"],
    textposition="outside"
  )

  # ------------------ LÍNEA KPI
  fig.add_scatter(
    x=df_group["MES"],
    y=df_group["KPI"],
    name="Ejecución %",
    mode="lines+markers+text",
    yaxis="y2",
    text=df_group["KPI"].map(lambda x: f"{x:.1f}%"),
    textposition="top center",
    line=dict(color="#2980b9", width=3)
  )

  # ------------------ LAYOUT FINAL
  fig.update_layout(
    title="📊 Histórico Ejecución MP",
    
    xaxis=dict(
        title="Mes",
        categoryorder="array",
        categoryarray=df_group["MES"]
    ),

    yaxis=dict(
        title="Cantidad"
    ),

    yaxis2=dict(
        title="%",
        overlaying="y",
        side="right",
        range=[0, 100]
    ),

    barmode="group",
    legend=dict(orientation="h"),
    margin=dict(t=50, b=40)
  )

  st.plotly_chart(fig, use_container_width=True)

