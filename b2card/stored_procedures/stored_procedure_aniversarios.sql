DROP PROCEDURE IF EXISTS aniversarios;
DELIMITER $$
CREATE PROCEDURE aniversarios ()
BEGIN

	DECLARE done INT DEFAULT FALSE;
	DECLARE id INT;
	DECLARE id_responsavel INT;
	DECLARE nome VARCHAR(100);
	
	DECLARE data_nascimento DATE;
	DECLARE dia INT;
	DECLARE mes INT;

	DECLARE TEXTO VARCHAR(1000);
	
	DECLARE id_responsaveis CURSOR FOR 
		SELECT pessoa_fisica_id FROM mensagens_responsavel
		WHERE tag = 'A';
	
	DECLARE funcionarios CURSOR FOR 
		SELECT p.nome_razao_social, MONTH(pf.data_nascimento), DAY(pf.data_nascimento) FROM cadastros_pessoafisica pf
		JOIN cadastros_pessoa p ON (p.id = pf.pessoa_id)
		JOIN cadastros_prestador pr ON (pf.id = pr.pessoa_fisica_id)
		WHERE (pr.data_inicio <= NOW() AND (data_fim >= NOW() OR data_fim IS NULL))
		AND MONTH(DATE_SUB(pf.data_nascimento, INTERVAL 15 DAY)) = MONTH(CURDATE())
		AND DAY(DATE_SUB(pf.data_nascimento, INTERVAL 15 DAY)) = DAY(CURDATE());
		
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
	
	SET TEXTO = "";
	
	OPEN funcionarios;
	
	read_loop: LOOP
	    FETCH funcionarios INTO nome, mes, dia;
	    IF done THEN
	      LEAVE read_loop;
	    END IF;
	    SET TEXTO = CONCAT(nome,'(', dia, '/', mes, '), ', TEXTO);
	  END LOOP;
	
	SELECT TEXTO;
	
	SET done = FALSE;
	
	CLOSE funcionarios;

	IF NULLIF(TEXTO, '') IS NOT NULL THEN
	
		OPEN id_responsaveis;
		
		read_loop: LOOP
		    FETCH id_responsaveis INTO id_responsavel;
		    IF done THEN
		      LEAVE read_loop;
		    END IF;
		    INSERT INTO mensagens_mensagem(pessoa_fisica_id, texto, lido, tag) 
			VALUES(id_responsavel, CONCAT('Aniversários: ', TEXTO), FALSE, 'E');
		    
		 END LOOP;
		  
		 CLOSE id_responsaveis;
		 
	END IF;
	
END $$
DELIMITER ;

CALL aniversarios;