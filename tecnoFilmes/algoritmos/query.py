
cargaAtividadesSql = ("INSERT INTO atividade (data, cliente_id)\
                        SELECT %s, C.codigo\
                        FROM clientes c\
                        LEFT JOIN pedidos p\
                            ON c.codigo = p.cliente_id\
                        LEFT JOIN atividade a\
                            ON c.codigo = a.cliente_id\
                        WHERE p.cliente_id IS NULL and a.cliente_id IS NULL")

sugestaoSql = "SELECT c.id, c.nome FROM atividade a \
                   INNER JOIN clientes c \
                        ON a.cliente_id = c.codigo \
                   WHERE a.usuario_id  IS NULL \
                   and (a.is_finalizada = false or a.is_finalizada IS NULL)  \
                   and (a.data <= now()) ORDER BY a.data DESC"

emAtendimentoSql = "SELECT c.id, c.nome FROM atividade a \
                        INNER JOIN clientes c \
                            ON a.cliente_id = c.codigo \
                        WHERE a.usuario_id = %s \
                        and (a.is_finalizada = false or a.is_finalizada IS NULL)"

emAtendimentoCincoSql = "SELECT c.id, c.nome FROM atividade a \
                        INNER JOIN clientes c \
                            ON a.cliente_id = c.codigo \
                        WHERE a.usuario_id = %s \
                        and (a.is_finalizada = false or a.is_finalizada IS NULL)\
                        and a.data > now() and a.data <= (now() + interval '5 days')"

sugestaoComPedidosSql = "SELECT DISTINCT c.codigo, c.nome, c.id, p.data\
                            FROM clientes c\
                            INNER JOIN pedidos p\
                                ON c.codigo = p.cliente_id\
                            WHERE p.data < now() and c.codigo NOT IN (select cliente_id from atividade a\
                                        WHERE (is_finalizada = false or is_finalizada IS NULL))\
                            ORDER BY c.codigo, p.data"
                
sugestaoCincoDiasSql = "SELECT c.id, c.nome FROM atividade a \
                        INNER JOIN clientes c\
                            ON c.codigo = a.cliente_id\
                        WHERE data > now() and data <= (now() + interval '5 days')"

ultimosPedidosSql = "SELECT p.data, p.op, p.material, p.comprimento, p.largura \
                    FROM clientes c\
                    INNER JOIN pedidos p \
	                    ON c.codigo = p.cliente_id \
                    WHERE c.id = %s\
                    ORDER BY p.data DESC LIMIT 5"                      