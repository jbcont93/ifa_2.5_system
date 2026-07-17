import 'package:flutter/material.dart';
import '../core/api_client.dart';
import 'partidas_screen.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});
  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  final _api = ApiClient();
  Map<String, dynamic>? _resumo;
  bool _carregando = true;

  @override
  void initState() {
    super.initState();
    _carregar();
  }

  Future<void> _carregar() async {
    setState(() => _carregando = true);
    try {
      final resumo = await _api.resumoDashboard();
      setState(() => _resumo = resumo);
    } finally {
      if (mounted) setState(() => _carregando = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Dashboard')),
      body: _carregando
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _carregar,
              child: ListView(
                padding: const EdgeInsets.all(16),
                children: [
                  GridView.count(
                    crossAxisCount: 2,
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    mainAxisSpacing: 12,
                    crossAxisSpacing: 12,
                    childAspectRatio: 1.6,
                    children: [
                      _kpiCard('Jogos Analisados', _resumo?['jogos_analisados']),
                      _kpiCard('Jogos Elite', _resumo?['jogos_elite']),
                      _kpiCard('Jogos Forte', _resumo?['jogos_forte']),
                      _kpiCard('Descartados', _resumo?['jogos_descartados']),
                    ],
                  ),
                  const SizedBox(height: 20),
                  FilledButton.icon(
                    onPressed: () => Navigator.of(context).push(
                      MaterialPageRoute(builder: (_) => const PartidasScreen()),
                    ),
                    icon: const Icon(Icons.list_alt),
                    label: const Text('Ver partidas Elite / Forte'),
                  ),
                ],
              ),
            ),
    );
  }

  Widget _kpiCard(String titulo, dynamic valor) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('${valor ?? '-'}', style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
            const SizedBox(height: 4),
            Text(titulo, style: const TextStyle(color: Colors.white60)),
          ],
        ),
      ),
    );
  }
}
