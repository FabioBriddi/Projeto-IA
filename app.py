import os
from flask import Flask, render_template, abort, url_for, request, jsonify, redirect, session, flash
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
import numpy as np
import json
import urllib.parse
import hashlib
from functools import wraps

from dotenv import load_dotenv
load_dotenv()

from google_maps_route import route as optimize_route_api

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_sessoes_strans' 

# --- CAMINHO ATUALIZADO ---
# Define o caminho base para a pasta de DataSets
if os.path.exists("C:\\UniSenac-IA\\STRANS-Projeto-IA\\DataSets"):
    DATASET_PATH = "C:\\UniSenac-IA\\STRANS-Projeto-IA\\DataSets"
else:
    base_dir = os.path.dirname(__file__)
    DATASET_PATH = os.path.join(base_dir, 'datasets')
    
MAPEAMENTO_DADOS = {
    'clientes': {'arquivo': 'strans_clientes.csv', 'titulo': 'Clientes'},
    'veiculos': {'arquivo': 'strans_veiculos.csv', 'titulo': 'Veículos'},
    'rotas': {'arquivo': 'strans_rotas.csv', 'titulo': 'Rotas'},
    'entregas': {'arquivo': 'strans_entregas.csv', 'titulo': 'Entregas'},
    'coletas': {'arquivo': 'strans_coletas.csv', 'titulo': 'Coletas'},
    'roteiro': {'arquivo': 'strans_roteiro.csv', 'titulo': 'Roteiro Otimizado'},
    'users': {'arquivo': 'strans_users.csv', 'titulo': 'Usuários'}
}

def ler_csv_limpo(caminho_arquivo, separador=','):
    try:
        df = pd.read_csv(caminho_arquivo, encoding='utf-8-sig', sep=separador)
    except UnicodeDecodeError:
        df = pd.read_csv(caminho_arquivo, encoding='latin-1', sep=separador)
    df.columns = df.columns.str.strip()
    return df

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_nome' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- ROTA DE LOGIN ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_user = request.form['login']
        senha_user = request.form['password']
        senha_md5 = hashlib.md5(senha_user.encode()).hexdigest()
        caminho_users_csv = os.path.join(DATASET_PATH, MAPEAMENTO_DADOS['users']['arquivo'])
        try:
            df_users = ler_csv_limpo(caminho_users_csv, separador=';')
            user_data = df_users[df_users['login'] == login_user]
            if not user_data.empty and user_data.iloc[0]['password'] == senha_md5:
                session['user_nome'] = user_data.iloc[0]['nome']
                session['has_api_key'] = str(user_data.iloc[0]['api_key']).lower() == 'true'
                return redirect(url_for('index'))
            else:
                flash('Login ou senha inválidos. Tente novamente.', 'error')
        except Exception as e:
            flash(f'Erro ao ler o arquivo de usuários: {e}', 'error')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- ROTAS DA APLICAÇÃO ---
@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/dados/<tipo_dado>')
@login_required
def mostrar_dados(tipo_dado):
    if tipo_dado not in MAPEAMENTO_DADOS or tipo_dado in ['coletas', 'roteiro', 'users']:
        abort(404)
    info = MAPEAMENTO_DADOS[tipo_dado]
    caminho_arquivo_csv = os.path.join(DATASET_PATH, info['arquivo'])
    try:
        df = ler_csv_limpo(caminho_arquivo_csv)
        tabela_html = df.to_html(classes='tabela-dados', index=False, table_id="tabelaDados", border=0)
    except Exception as e:
        abort(500, description=f"Ocorreu um erro ao processar o arquivo: {e}")
    return render_template('dados.html', titulo=info['titulo'], tabela_html=tabela_html)

@app.route('/coletas')
@login_required
def coletas():
    info = MAPEAMENTO_DADOS['coletas']
    caminho_arquivo_csv = os.path.join(DATASET_PATH, info['arquivo'])
    try:
        df = ler_csv_limpo(caminho_arquivo_csv, separador=';')
        dados_coletas = df.to_dict('records')
        headers = df.columns.tolist()
    except Exception as e:
        abort(500, description=f"Ocorreu um erro ao processar o arquivo de coletas: {e}")
    return render_template('coletas.html', titulo=info['titulo'], headers=headers, coletas=dados_coletas)

@app.route('/roteiro')
@login_required
def roteiro():
    caminho_arquivo_csv = os.path.join(DATASET_PATH, 'strans_roteiro.csv')
    google_maps_url = None
    tipo_roteiro = session.get('last_route_type', 'Gerado')
    titulo = f"Roteiro {tipo_roteiro}"
    try:
        if not os.path.exists(caminho_arquivo_csv) or os.path.getsize(caminho_arquivo_csv) == 0:
            return render_template('roteiro.html', titulo="Roteiro de Coleta", roteiro=None, headers=None, google_maps_url=None)
        df = ler_csv_limpo(caminho_arquivo_csv, separador=';')
        dados_roteiro = df.to_dict('records')
        headers = df.columns.tolist()
        if not df.empty and len(df) >= 2:
            enderecos = df['endereco'].tolist()
            origin = urllib.parse.quote_plus(enderecos[0])
            destination = urllib.parse.quote_plus(enderecos[-1])
            waypoints = ""
            if len(enderecos) > 2:
                waypoints_list = [urllib.parse.quote_plus(addr) for addr in enderecos[1:-1]]
                waypoints = "|".join(waypoints_list)
            google_maps_url = f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}&waypoints={waypoints}"
            with open(os.path.join(DATASET_PATH, 'strans_maps_envio.txt'), 'w') as f:
                f.write(google_maps_url)
    except Exception as e:
        abort(500, description=f"Ocorreu um erro ao processar o arquivo de roteiro: {e}")
    return render_template('roteiro.html', titulo=titulo, headers=headers, roteiro=dados_roteiro, google_maps_url=google_maps_url)

@app.route('/gerar_roteiro', methods=['POST'])
@login_required
def gerar_roteiro():
    try:
        data = request.get_json()
        selected_ids = data.get('ids', [])
        if not selected_ids:
            return jsonify({'success': False, 'message': 'Nenhuma coleta selecionada.'}), 400
        
        caminho_coletas_csv = os.path.join(DATASET_PATH, 'strans_coletas.csv')
        df_coletas = ler_csv_limpo(caminho_coletas_csv, separador=';')
        
        start_point = df_coletas[df_coletas['ID_Coleta'] == 'CO000']
        end_point = df_coletas[df_coletas['ID_Coleta'] == 'CO999']
        waypoints_df = df_coletas[df_coletas['ID_Coleta'].isin(selected_ids)]

        if start_point.empty or end_point.empty:
             return jsonify({'success': False, 'message': 'Ponto de partida (CO000) ou chegada (CO999) não encontrado.'}), 400

        origin_address = start_point.iloc[0]['Endereco_Coleta']
        destination_address = end_point.iloc[0]['Endereco_Coleta']
        waypoints_addresses = waypoints_df['Endereco_Coleta'].tolist()

        use_paid_api = session.get('has_api_key', False)
        
        if use_paid_api and os.getenv("GOOGLE_MAPS_API_KEY"):
            session['last_route_type'] = 'Otimizado'
        else:
            session['last_route_type'] = 'Gerado'

        optimized_route = optimize_route_api(
            origin=origin_address,
            destination=destination_address,
            waypoints=waypoints_addresses,
            optimize_waypoints=True,
            use_paid_api=use_paid_api
        )
        
        final_route = []
        final_route.append({'id': 'CO000', 'ordem': 0, 'nome': start_point.iloc[0]['Nome'], 'endereco': start_point.iloc[0]['Endereco_Coleta']})
        for i, waypoint_index in enumerate(optimized_route.waypoint_order):
            waypoint_info = waypoints_df.iloc[waypoint_index]
            final_route.append({'id': waypoint_info['ID_Coleta'], 'ordem': i + 1, 'nome': waypoint_info['Nome'], 'endereco': waypoint_info['Endereco_Coleta']})
        final_route.append({'id': 'CO999', 'ordem': len(final_route), 'nome': end_point.iloc[0]['Nome'], 'endereco': end_point.iloc[0]['Endereco_Coleta']})
        
        df_roteiro = pd.DataFrame(final_route)
        caminho_roteiro_csv = os.path.join(DATASET_PATH, 'strans_roteiro.csv')
        df_roteiro.to_csv(caminho_roteiro_csv, index=False, sep=';', encoding='latin-1')
        
        return jsonify({'success': True, 'redirect_url': url_for('roteiro')})

    except Exception as e:
        print(f"ERRO ao gerar roteiro: {e}")
        return jsonify({'success': False, 'message': f'Erro interno do servidor: {e}'}), 500

# --- ROTAS DE ANÁLISE ---
@app.route('/analise_clientes')
@login_required
def analise_clientes():
    try:
        caminho_arquivo = os.path.join(DATASET_PATH, 'strans_clientes.csv')
        df = ler_csv_limpo(caminho_arquivo)
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        df['cluster'] = kmeans.fit_predict(df[['volume_mensal_entregas']])
        cluster_centers = kmeans.cluster_centers_.flatten()
        descriptions = ["(Baixo Volume)", "(Médio Volume)", "(Alto Volume)"]
        cluster_map = { list(cluster_centers).index(c): f"Nível {i+1} {descriptions[i]}" for i, c in enumerate(sorted(cluster_centers)) }
        df['classificacao_volume'] = df['cluster'].map(cluster_map)
        sns.set_style("whitegrid")
        caminho_base_graficos = os.path.join(app.static_folder, 'analise')
        if not os.path.exists(caminho_base_graficos): os.makedirs(caminho_base_graficos)
        plt.figure(figsize=(10, 6)); sns.barplot(data=df, x='tipo_cliente', y='volume_mensal_entregas', estimator=sum, ci=None, palette='viridis'); plt.title('Volume Total de Entregas por Tipo de Cliente', fontsize=16); plt.ylabel('Volume Total de Entregas'); plt.xlabel('Tipo de Cliente'); plt.xticks(rotation=45); plt.savefig(os.path.join(caminho_base_graficos, 'grafico1.png'), bbox_inches='tight'); plt.close()
        plt.figure(figsize=(10, 6)); sns.barplot(data=df, x='porte_empresa', y='volume_mensal_entregas', estimator=sum, ci=None, palette='plasma', order=['Pequeno', 'Médio', 'Grande']); plt.title('Volume Total de Entregas por Porte da Empresa', fontsize=16); plt.ylabel('Volume Total de Entregas'); plt.xlabel('Porte da Empresa'); plt.savefig(os.path.join(caminho_base_graficos, 'grafico2.png'), bbox_inches='tight'); plt.close()
        plt.figure(figsize=(10, 6)); sns.barplot(data=df, x='regiao', y='volume_mensal_entregas', estimator=sum, ci=None, palette='magma'); plt.title('Volume Total de Entregas por Região', fontsize=16); plt.ylabel('Volume Total de Entregas'); plt.xlabel('Região'); plt.savefig(os.path.join(caminho_base_graficos, 'grafico3.png'), bbox_inches='tight'); plt.close()
        urls_graficos = { 'grafico1': url_for('static', filename='analise/grafico1.png'), 'grafico2': url_for('static', filename='analise/grafico2.png'), 'grafico3': url_for('static', filename='analise/grafico3.png') }
        resumo_classificacao = df.groupby('classificacao_volume')['volume_mensal_entregas'].agg(['mean', 'count']).round(0); resumo_classificacao.columns = ['Volume Médio', 'Nº de Clientes']; resumo_classificacao = resumo_classificacao.sort_values(by='Volume Médio')
    except Exception as e:
        abort(500, description=f"Ocorreu um erro ao gerar a análise de clientes: {e}")
    return render_template('analise_clientes.html', graficos=urls_graficos, resumo=resumo_classificacao.to_html(classes='tabela-dados'))

@app.route('/analise_entregas_volumes')
@login_required
def analise_entregas_volumes():
    try:
        caminho_arquivo = os.path.join(DATASET_PATH, 'strans_entregas.csv')
        df = ler_csv_limpo(caminho_arquivo)
        df_2024 = df[df['ano'] == 2024].copy()
        sns.set_style("whitegrid")
        caminho_base_graficos = os.path.join(app.static_folder, 'analise')
        total_pequenas = df_2024['entregas_pequenas'].sum(); total_grandes = df_2024['entregas_grandes'].sum()
        plt.figure(figsize=(8, 6)); sns.barplot(x=['Entregas Pequenas', 'Entregas Grandes'], y=[total_pequenas, total_grandes], palette='coolwarm'); plt.title('Comparativo Anual de Entregas (2024)', fontsize=16); plt.ylabel('Volume Total'); plt.savefig(os.path.join(caminho_base_graficos, 'grafico_entregas_anual.png'), bbox_inches='tight'); plt.close()
        plt.figure(figsize=(12, 6)); plt.plot(df_2024['mes'], df_2024['entregas_pequenas'], marker='o', linestyle='-', label='Entregas Pequenas'); plt.plot(df_2024['mes'], df_2024['entregas_grandes'], marker='o', linestyle='-', label='Entregas Grandes'); plt.title('Evolução Mensal de Entregas (2024)', fontsize=16); plt.xlabel('Mês'); plt.ylabel('Número de Entregas'); plt.xticks(range(1, 13)); plt.legend(); plt.grid(True); plt.savefig(os.path.join(caminho_base_graficos, 'grafico_entregas_mensal.png'), bbox_inches='tight'); plt.close()
        X = df_2024[['mes']]; y_pequenas = df_2024['entregas_pequenas']; y_grandes = df_2024['entregas_grandes']
        model_pequenas = LinearRegression().fit(X, y_pequenas); model_grandes = LinearRegression().fit(X, y_grandes)
        plt.figure(figsize=(12, 6)); sns.regplot(x='mes', y='entregas_pequenas', data=df_2024, ci=None, label='Tendência - Pequenas', scatter_kws={'alpha':0.5}); sns.regplot(x='mes', y='entregas_grandes', data=df_2024, ci=None, label='Tendência - Grandes', scatter_kws={'alpha':0.5}); plt.title('Previsão de Tendência de Entregas (Machine Learning)', fontsize=16); plt.xlabel('Mês (1-12: 2024, 13-15: Previsão 2025)'); plt.ylabel('Número de Entregas'); plt.legend(); plt.grid(True); plt.savefig(os.path.join(caminho_base_graficos, 'grafico_entregas_previsao.png'), bbox_inches='tight'); plt.close()
        urls_graficos = { 'anual': url_for('static', filename='analise/grafico_entregas_anual.png'), 'mensal': url_for('static', filename='analise/grafico_entregas_mensal.png'), 'previsao': url_for('static', filename='analise/grafico_entregas_previsao.png') }
    except Exception as e:
        abort(500, description=f"Ocorreu um erro ao gerar a análise de entregas: {e}")
    return render_template('analise_entregas.html', graficos=urls_graficos)

@app.route('/analise_veiculos')
@login_required
def analise_veiculos():
    try:
        caminho_arquivo = os.path.join(DATASET_PATH, 'strans_entregas.csv')
        df = ler_csv_limpo(caminho_arquivo)
        df_2024 = df[df['ano'] == 2024].copy()
        veiculos = ['entregas_moto', 'entregas_bike', 'entregas_van', 'entregas_caminhao']
        veiculos_nomes = ['Moto', 'Bike', 'Van', 'Caminhão']
        sns.set_style("whitegrid")
        caminho_base_graficos = os.path.join(app.static_folder, 'analise')
        totais_veiculos = [df_2024[v].sum() for v in veiculos]
        plt.figure(figsize=(10, 6)); sns.barplot(x=veiculos_nomes, y=totais_veiculos, palette='cubehelix'); plt.title('Comparativo Anual por Tipo de Veículo (2024)', fontsize=16); plt.ylabel('Volume Total de Entregas'); plt.savefig(os.path.join(caminho_base_graficos, 'grafico_veiculos_anual.png'), bbox_inches='tight'); plt.close()
        plt.figure(figsize=(12, 7)); 
        for v, nome in zip(veiculos, veiculos_nomes):
            plt.plot(df_2024['mes'], df_2024[v], marker='o', linestyle='-', label=nome)
        plt.title('Evolução Mensal por Tipo de Veículo (2024)', fontsize=16); plt.xlabel('Mês'); plt.ylabel('Número de Entregas'); plt.xticks(range(1, 13)); plt.legend(); plt.grid(True); plt.savefig(os.path.join(caminho_base_graficos, 'grafico_veiculos_mensal.png'), bbox_inches='tight'); plt.close()
        plt.figure(figsize=(12, 7));
        for v, nome in zip(veiculos, veiculos_nomes):
             sns.regplot(x='mes', y=v, data=df_2024, ci=None, label=f'Tendência - {nome}', scatter_kws={'alpha':0.4})
        plt.title('Previsão de Tendência por Veículo (Machine Learning)', fontsize=16); plt.xlabel('Mês (1-12: 2024)'); plt.ylabel('Número de Entregas'); plt.legend(); plt.grid(True); plt.savefig(os.path.join(caminho_base_graficos, 'grafico_veiculos_previsao.png'), bbox_inches='tight'); plt.close()
        urls_graficos = { 'anual': url_for('static', filename='analise/grafico_veiculos_anual.png'), 'mensal': url_for('static', filename='analise/grafico_veiculos_mensal.png'), 'previsao': url_for('static', filename='analise/grafico_veiculos_previsao.png') }
    except Exception as e:
        abort(500, description=f"Ocorreu um erro ao gerar a análise de veículos: {e}")
    return render_template('analise_veiculos.html', graficos=urls_graficos)


@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return "<h1>404 - Página não encontrada</h1><p>A URL que você tentou acessar não existe.</p><a href='/'>Voltar</a>", 404

@app.errorhandler(500)
def erro_interno(e):
    return f"<h1>500 - Erro Interno do Servidor</h1><p>{e.description}</p><a href='/'>Voltar</a>", 500


if __name__ == '__main__':
    app.run(debug=True)
