// Recebimento Buffer - Ruas 21 a 26
(function () {
    if (!window.initialData) {
        window.initialData = [];
    }

    const bufferConfigs = [
        { rua: '21', lados: { B: { posicoes: 18, niveis: 4 } } },
        { rua: '22', lados: { A: { posicoes: 18, niveis: 4 }, B: { posicoes: 18, niveis: 5 } } },
        { rua: '23', lados: { A: { posicoes: 18, niveis: 5 }, B: { posicoes: 18, niveis: 5 } } },
        { rua: '24', lados: { A: { posicoes: 18, niveis: 5 }, B: { posicoes: 18, niveis: 5 } } },
        { rua: '25', lados: { A: { posicoes: 18, niveis: 5 }, B: { posicoes: 18, niveis: 4 } } },
        { rua: '26', lados: { A: { posicoes: 18, niveis: 4 } } }
    ];

    const bufferEntries = [];

    bufferConfigs.forEach(({ rua, lados }) => {
        Object.entries(lados).forEach(([lado, { posicoes, niveis }]) => {
            for (let nivel = 1; nivel <= niveis; nivel++) {
                for (let posicao = 1; posicao <= posicoes; posicao++) {
                    const codigo = `BU${rua}${lado}${String(posicao).padStart(2, '0')}${String(nivel).padStart(2, '0')}`;
                    bufferEntries.push({
                        codigo,
                        descricao: `RECEBIMENTO BUFFER - RUA ${rua}`,
                        custom1: '',
                        custom2: '',
                        custom3: ''
                    });
                }
            }
        });
    });

    window.initialData = window.initialData.concat(bufferEntries);
})();
