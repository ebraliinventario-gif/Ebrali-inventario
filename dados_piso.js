// Posições de PISO
(function () {
    if (!window.initialData) {
        window.initialData = [];
    }

    const pisoEntries = [
        { codigo: 'PS01P0000', descricao: 'PISO ESTOQUE - RUA 01' },
        { codigo: 'PS02P0000', descricao: 'PISO ESTOQUE - RUA 02' },
        { codigo: 'PS03P0000', descricao: 'PISO ESTOQUE - RUA 03' },
        { codigo: 'PS04P0000', descricao: 'PISO ESTOQUE - RUA 04' },
        { codigo: 'PS05P0000', descricao: 'PISO ESTOQUE - RUA 05' },
        { codigo: 'PS06P0000', descricao: 'PISO ESTOQUE - RUA 06' },
        { codigo: 'PS07P0000', descricao: 'PISO ESTOQUE - RUA 07' },
        { codigo: 'PS08P0000', descricao: 'PISO ESTOQUE - RUA 08' },
        { codigo: 'PS09B0000', descricao: 'PISO ESTOQUE - RUA 09' },
        { codigo: 'PS10B0000', descricao: 'PISO ESTOQUE - RUA 10' },
        { codigo: 'PS11B0000', descricao: 'PISO ESTOQUE - RUA 11' },
        { codigo: 'PS12B0000', descricao: 'PISO ESTOQUE - RUA 12' },
        { codigo: 'PS13B0000', descricao: 'PISO ESTOQUE - RUA 13' },
        { codigo: 'PS14B0000', descricao: 'PISO ESTOQUE - RUA 14' },
        { codigo: 'PS15B0000', descricao: 'PISO ESTOQUE - RUA 15' },
        { codigo: 'PS16B0000', descricao: 'PISO ESTOQUE - RUA 16' },
        { codigo: 'PS17P0000', descricao: 'PISO ESTOQUE - RUA 17' },
        { codigo: 'PS18P0000', descricao: 'PISO ESTOQUE - RUA 18' },
        { codigo: 'PS19P0000', descricao: 'PISO ESTOQUE - RUA 19' },
        { codigo: 'PS20P0000', descricao: 'PISO ESTOQUE - RUA 20' },
        { codigo: 'PS21P0000', descricao: 'PISO REC. BUFFER - RUA 21' },
        { codigo: 'PS22P0000', descricao: 'PISO REC. BUFFER - RUA 22' },
        { codigo: 'PS23P0000', descricao: 'PISO REC. BUFFER - RUA 23' },
        { codigo: 'PS24P0000', descricao: 'PISO REC. BUFFER - RUA 24' },
        { codigo: 'PS25P0000', descricao: 'PISO REC. BUFFER - RUA 25' },
        { codigo: 'PS26P0000', descricao: 'PISO RECEBIMENTO BUFFER - RUA 26' },
        { codigo: 'PS27P0000', descricao: 'PISO INDUSTRIA - RUA 27' },
        { codigo: 'PS28P0000', descricao: 'PISO INDUSTRIA - RUA 28' }
    ];

    window.initialData = window.initialData.concat(
        pisoEntries.map(item => ({
            codigo: item.codigo,
            descricao: item.descricao,
            custom1: '',
            custom2: '',
            custom3: ''
        }))
    );
})();
