// Indústria 99 - Ruas 27 e 28
(function () {
    if (!window.initialData) {
        window.initialData = [];
    }

    const industriaConfig = [
        { rua: '27', lado: 'B', niveis: 3 },
        { rua: '28', lado: 'A', niveis: 3 },
        { rua: '28', lado: 'B', niveis: 3 }
    ];

    const entries = [];

    industriaConfig.forEach(({ rua, lado, niveis }) => {
        for (let posicao = 1; posicao <= 16; posicao++) {
            for (let nivel = 1; nivel <= niveis; nivel++) {
                const codigo = `ID${rua}${lado}${String(posicao).padStart(2, '0')}${String(nivel).padStart(2, '0')}`;
                entries.push({
                    codigo,
                    descricao: `INDUSTRIA 99 - RUA ${rua}`,
                    custom1: '',
                    custom2: '',
                    custom3: ''
                });
            }
        }
    });

    window.initialData = window.initialData.concat(entries);
})();
