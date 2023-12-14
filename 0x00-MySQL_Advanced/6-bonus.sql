-- create a stored procedure that adds a new correction for a student
DELIMITER //
CREATE PROCEDURE AddBonus (IN user_id INT, IN project_name VARCHAR(255), IN score INT)
BEGIN
DECLARE project_id INT;

-- Retrieve the project_id based on the project_naem
SELECT id INTO project_id FROM projects WHERE name = project_name;

-- IF project_id is null, insert a new row in the projects table
IF project_id IS  NULL THEN
    INSERT INTO projects (name) VALUES (project_name);
    SELECT id INTO project_id FROM projects WHERE name = project_name;
    END IF;
-- Insert the new correction into the corrections table
INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, project_id, score);
END //
DELIMITER ;
