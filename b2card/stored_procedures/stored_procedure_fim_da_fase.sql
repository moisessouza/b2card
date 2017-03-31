DROP PROCEDURE IF EXISTS fim_de_fase;
DELIMITER $$
CREATE PROCEDURE fim_de_fase ()
BEGIN

	DECLARE done_demanda INT DEFAULT FALSE;
	DECLARE id INT;
	DECLARE nome_demanda VARCHAR(100);
	DECLARE descricao VARCHAR(100);
	DECLARE data_fim DATE;
	
	DECLARE demanda_fase CURSOR FOR 
		SELECT d.id, d.nome_demanda, f.descricao, fa.data_fim FROM demandas_demanda d
			JOIN demandas_faseatividade fa ON (d.id = fa.demanda_id) 
			JOIN cadastros_fase f ON (fa.fase_id = f.id)
			WHERE fa.data_fim = DATE_SUB(CURDATE(), INTERVAL 15 DAY)
			OR fa.data_fim = DATE_SUB(CURDATE(), INTERVAL 2 DAY);
		
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done_demanda = TRUE;
	
	OPEN demanda_fase;

	loop_demanda_fase: LOOP
	    FETCH demanda_fase INTO id, nome_demanda, descricao, data_fim;
	    IF done_demanda THEN
	      LEAVE loop_demanda_fase;
	    END IF;

	    SELECT id;
	    
	    bloco_responsavel: BEGIN
	    
		DECLARE responsavel_id INT;
		DECLARE done_responsavel INT DEFAULT FALSE;
		DECLARE responsavel CURSOR FOR
			SELECT pf.id FROM cadastros_pessoafisica pf
			JOIN cadastros_pessoa p ON (p.id = pf.pessoa_id)
			JOIN demandas_demanda d ON (d.responsavel_id = pf.id)
			WHERE d.id=id;
			
		DECLARE CONTINUE HANDLER FOR NOT FOUND SET done_responsavel = TRUE;
		
		OPEN responsavel;
		
		loop_responsavel: LOOP
			FETCH responsavel INTO responsavel_id;
			IF done_responsavel THEN
			    LEAVE loop_responsavel;
			END IF;
			INSERT INTO mensagens_mensagem(pessoa_fisica_id, data_criacao, origem, texto, lido, tag) 
			VALUES(responsavel_id, CURDATE(), 'SISTEMA', 
				CONCAT('Fase perto do fim: demanda - ', LPAD(id,5,'0'), ' - ', nome_demanda, ' - fase - ', descricao, ' - ', DATE_FORMAT(data_fim, '%d/%m/%Y')), 
				FALSE, 'F');
		 END LOOP loop_responsavel;
		 
		 CLOSE responsavel;
	    
	    END bloco_responsavel;
	    
	  END LOOP loop_demanda_fase;
	  
	CLOSE demanda_fase;
	
END $$
DELIMITER ;

CALL fim_de_fase;

DROP EVENT IF EXISTS fim_de_fase_event;
CREATE EVENT fim_de_fase_event
  ON SCHEDULE
    EVERY 1 DAY
    STARTS '2017-03-30 01:00:00' ON COMPLETION PRESERVE ENABLE 
  DO
  	CALL fim_de_fase;