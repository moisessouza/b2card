DROP PROCEDURE IF EXISTS renegociacao;
DELIMITER $$
CREATE PROCEDURE renegociacao ()
BEGIN

	DECLARE done INT DEFAULT FALSE;
	DECLARE nome VARCHAR(100);
	DECLARE data_renegociacao DATE;
	DECLARE id_responsavel INT;
	
	DECLARE TEXTO VARCHAR(1000);
	
	DECLARE id_responsaveis CURSOR FOR 
		SELECT pessoa_fisica_id FROM mensagens_responsavel
		WHERE tag = 'R' AND ativo=TRUE;
	
	DECLARE renegociacao CURSOR FOR 
		SELECT nome_razao_social, data_renegociacao_valor 
		FROM cadastros_pessoa WHERE data_renegociacao_valor IS NULL 
		OR data_renegociacao_valor <= CURDATE(); 
		
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
	
	DELETE FROM mensagens_mensagem WHERE tag='R';
	
	OPEN renegociacao;

	SET TEXTO = '';	
	
	read_loop: LOOP
	    FETCH renegociacao INTO nome, data_renegociacao;
	    IF done THEN
	      LEAVE read_loop;
	    END IF;
	    SET TEXTO = CONCAT(nome, '(', IF(data_renegociacao IS NOT NULL, DATE_FORMAT(data_renegociacao, '%d/%m/%Y'),'Sem data'), '), ', TEXTO);
	  END LOOP;
	  
	CLOSE renegociacao;

	SET done = FALSE;	
	
	IF NULLIF(TEXTO, '') IS NOT NULL THEN

		OPEN id_responsaveis;

		read_loop: LOOP
		    FETCH id_responsaveis INTO id_responsavel;
		    IF done THEN
		      LEAVE read_loop;
		    END IF;
		    INSERT INTO mensagens_mensagem(pessoa_fisica_id, data_criacao, origem, texto, lido, tag) 
			VALUES(id_responsavel, CURDATE(), 'SISTEMA', CONCAT('Renegociações pendentes: ', TEXTO), FALSE, 'R');
		    
		 END LOOP;
		  
		 CLOSE id_responsaveis;
		
	END IF;	
END $$
DELIMITER ;

CALL renegociacao;

DROP EVENT IF EXISTS renegociacao_event;
CREATE EVENT renegociacao_event
  ON SCHEDULE
    EVERY 1 DAY
    STARTS '2017-03-30 01:00:00' ON COMPLETION PRESERVE ENABLE 
  DO
  	CALL renegociacao;