CREATE SCHEMA IF NOT EXISTS service_handler;
USE service_handler;

CREATE TABLE SampleEntityStatus(
    id		               INT NOT NULL UNIQUE AUTO_INCREMENT,
    enumerator             VARCHAR(50) NOT NULL,
    created_at             TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE UC_sample_entity_status_enumerator (enumerator)
);

INSERT INTO SampleEntityStatus (enumerator) VALUES
	 ('created'),
	 ('success'),
     ('failed');

CREATE TABLE SampleEntity(
    id                     INT NOT NULL UNIQUE AUTO_INCREMENT,
    sample_entity_key      VARCHAR(36) NOT NULL,
    requester_key          VARCHAR(36) NOT NULL,
    status_id              INT NOT NULL,
    sample_entity_data     JSON NOT NULL,
    created_at             TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    CONSTRAINT fk_sample_entity_status_id FOREIGN KEY (status_id) REFERENCES SampleEntityStatus(id)
);

CREATE TABLE SampleEntityStatusEvent(
    id                      INT NOT NULL UNIQUE AUTO_INCREMENT,
    sample_entity_id              INT  NOT NULL,
    status_id               INT NOT NULL,
    event_date              DATETIME NOT NULL,
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    CONSTRAINT fk_sample_entity_status_event_status_id FOREIGN KEY (status_id) REFERENCES SampleEntityStatus(id),
    CONSTRAINT fk_sample_entity_status_event_sample_entity_id FOREIGN KEY (sample_entity_id) REFERENCES SampleEntity(id)
);

CREATE TABLE SampleXml(
    id                      INT NOT NULL UNIQUE AUTO_INCREMENT,
    xml_data                JSON NOT NULL,
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);
