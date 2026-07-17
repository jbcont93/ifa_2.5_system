class RelatorioAnalitico {
  final int idPartida;
  final String campeonato;
  final String mandante;
  final String visitante;
  final double ifaMandante;
  final double ifaVisitante;
  final double iaGeral;
  final double consenso;
  final String classificacao;
  final String? grauRisco;
  final String cenarioPrincipal;
  final double probVitoriaMandante;
  final double probEmpate;
  final double probVitoriaVisitante;

  RelatorioAnalitico({
    required this.idPartida,
    required this.campeonato,
    required this.mandante,
    required this.visitante,
    required this.ifaMandante,
    required this.ifaVisitante,
    required this.iaGeral,
    required this.consenso,
    required this.classificacao,
    required this.grauRisco,
    required this.cenarioPrincipal,
    required this.probVitoriaMandante,
    required this.probEmpate,
    required this.probVitoriaVisitante,
  });

  factory RelatorioAnalitico.fromJson(Map<String, dynamic> json) {
    final probs = json['probabilidades'] as Map<String, dynamic>;
    return RelatorioAnalitico(
      idPartida: json['id_partida'],
      campeonato: json['campeonato'],
      mandante: json['mandante'],
      visitante: json['visitante'],
      ifaMandante: (json['ifa_mandante'] as num).toDouble(),
      ifaVisitante: (json['ifa_visitante'] as num).toDouble(),
      iaGeral: (json['ia_geral'] as num).toDouble(),
      consenso: (json['consenso'] as num).toDouble(),
      classificacao: json['classificacao'],
      grauRisco: json['grau_risco'],
      cenarioPrincipal: json['cenario_principal'],
      probVitoriaMandante: (probs['prob_vitoria_mandante'] as num).toDouble(),
      probEmpate: (probs['prob_empate'] as num).toDouble(),
      probVitoriaVisitante: (probs['prob_vitoria_visitante'] as num).toDouble(),
    );
  }
}
