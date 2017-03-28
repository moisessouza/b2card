DROP TABLE IF EXISTS tbl_exame_periodico;
CREATE TABLE tbl_exame_periodico (
	id INT NOT NULL AUTO_INCREMENT,
	pessoa_fisica_id INT NOT NULL,
	feito INT NULL,
	PRIMARY KEY (id)
);

DROP PROCEDURE IF EXISTS exame_periodico;
DELIMITER $$
CREATE PROCEDURE exame_periodico ()
BEGIN

	DECLARE done INT DEFAULT FALSE;
	DECLARE id INT;
	DECLARE id_responsavel INT;
	DECLARE nome VARCHAR(100);

	DECLARE TEXTO VARCHAR(1000);
	
	DECLARE id_responsaveis CURSOR FOR 
		SELECT pessoa_fisica_id FROM mensagens_responsavel
		WHERE tag = 'E';
	
	DECLARE funcionarios CURSOR FOR 
		SELECT p.nome_razao_social, pf.id FROM cadastros_pessoafisica pf
		JOIN cadastros_pessoa p ON (p.id = pf.pessoa_id)
		JOIN cadastros_prestador pr ON (pf.id = pr.pessoa_fisica_id)
		WHERE (pr.data_inicio <= NOW() AND (data_fim >= NOW() OR data_fim IS NULL))
		AND data_ultimo_exame_periodico <= DATE_ADD(DATE_SUB(CURDATE(),INTERVAL 1 YEAR), INTERVAL 1 MONTH)
		AND pf.id NOT IN (SELECT pessoa_fisica_id FROM tbl_exame_periodico WHERE feito=FALSE OR feito IS NULL);
		
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
	
	SET TEXTO = "";
	
	OPEN funcionarios;
	
	read_loop: LOOP
	    FETCH funcionarios INTO nome, id;
	    IF done THEN
	      LEAVE read_loop;
	    END IF;
	    SET TEXTO = CONCAT(nome, ', ', TEXTO);
	    INSERT INTO tbl_exame_periodico(pessoa_fisica_id, feito) VALUES (id, FALSE);
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
		    INSERT INTO mensagens_mensagem(pessoa_fisica_id, data_criacao, texto, lido, tag) 
			VALUES(id_responsavel, CURDATE(), CONCAT('Exames periódicos: ', TEXTO), FALSE, 'E');
		    
		 END LOOP;
		  
		 CLOSE id_responsaveis;
		 
	END IF;
	
	UPDATE tbl_exame_periodico SET feito = TRUE WHERE pessoa_fisica_id IN (
			SELECT pf.id FROM cadastros_pessoafisica pf
			JOIN cadastros_pessoa p ON (p.id = pf.pessoa_id)
			JOIN cadastros_prestador pr ON (pf.id = pr.pessoa_fisica_id)
			WHERE (pr.data_inicio <= NOW() AND (data_fim >= NOW() OR data_fim IS NULL))
			AND data_ultimo_exame_periodico > NOW()
		 );

END $$
DELIMITER ;

CALL exame_periodico;