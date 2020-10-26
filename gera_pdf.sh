# this script merge the markdown templates with the coments,
# generating a markdown file for each discipline, and the
# corresponding generated pdf will be in /reports

rm -r relatorios/
mkdir relatorios

rm -r relatorios/feedback_consulta.md
touch relatorios/feedback_consulta.md

echo '-- GERANDO PDFS'

for d in disciplinas/*/; do
    cd "$d"
    echo $d
    # juntando arquivos numa coisa só
    cat name.md \
        ../../templates/ensino_remoto.md \
        rmt_cmt.md \
        ../../templates/ensino_geral.md \
        gen_cmt.md >report.md

    # gera os PDFs com os graficos e os comentarios
    #pandoc -V geometry:margin=.3in report.md ../../relatorios/${d%?}.pdf
    name=${d:12}
    name=${name%?}
    pandoc -V geometry:margin=.3in -f markdown report.md -t latex -o ../../relatorios/$name.pdf

    # arquivo para o feedback da consulta
    cat ../../relatorios/feedback_consulta.md con_cmt.md > ../../feedback_consulta.md

    cd ../..
done
