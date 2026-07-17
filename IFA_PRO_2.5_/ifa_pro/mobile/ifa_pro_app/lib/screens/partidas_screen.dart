import 'package:flutter/material.dart';
import '../core/api_client.dart';
import '../core/theme.dart';
import '../models/relatorio_analitico.dart';

/// Lista as partidas classificadas como Elite ou Forte pelo Motor de
/// Consenso — a mesma lista oficial de saida do sistema (secao 7).
class PartidasScreen extends StatefulWidget {
  const PartidasScreen({super.key});
  @override
  State<PartidasScreen> createState() => _PartidasScreenState();
}

class _PartidasScreenState extends State<PartidasScreen> {
  final _api = ApiClient();
  List<RelatorioAnalitico> _relatorios = [];
  bool _carregando = true;

  @override
  void initState() {
    super.initState();
    _carregar();
  }

  Future<void> _carregar() async {
    setState(() => _carregando = true);
    final dados = await _api.listarEliteEForte();
    setState(() {
      _relatorios = dados.map((e) => RelatorioAnalitico.fromJson(e)).toList();
      _carregando = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Partidas Elite / Forte')),
      body: _carregando
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _carregar,
              child: ListView.builder(
                padding: const EdgeInsets.all(12),
                itemCount: _relatorios.length,
                itemBuilder: (context, i) {
                  final r = _relatorios[i];
                  return Card(
                    child: ListTile(
                      leading: CircleAvatar(
                        backgroundColor: IfaTheme.corClassificacao(r.classificacao),
                        child: Text(r.consenso.toStringAsFixed(0)),
                      ),
                      title: Text('${r.mandante} x ${r.visitante}'),
                      subtitle: Text('${r.campeonato} · ${r.classificacao} · ${r.cenarioPrincipal}'),
                      trailing: Text('${r.consenso}'),
                    ),
                  );
                },
              ),
            ),
    );
  }
}
