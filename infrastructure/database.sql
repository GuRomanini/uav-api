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

CREATE TABLE ServiceType(
    id                          INT NOT NULL UNIQUE AUTO_INCREMENT,
    enumerator                  VARCHAR(50) NOT NULL UNIQUE,
    created_at                  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id)
);

INSERT INTO ServiceType (enumerator) VALUES
    ('command'),
    ('data'),
    ('event'),
    ('stream');

CREATE TABLE Service(
    id                          INT NOT NULL UNIQUE AUTO_INCREMENT,
    service_key                 CHAR(36) NOT NULL UNIQUE,
    service_type_id             INT NOT NULL,
    created_at                  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_service_type_service FOREIGN KEY (service_type_id)
        REFERENCES ServiceType(id)
);

CREATE TABLE ServiceRequestStatus(
    id                          INT NOT NULL UNIQUE AUTO_INCREMENT,
    enumerator                  VARCHAR(50) NOT NULL UNIQUE,
    created_at                  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id)
);

INSERT INTO ServiceRequestStatus (enumerator) VALUES
	 ('on_queue'),
	 ('in_progress'),
	 ('completed'),
     ('cancelled'),
     ('aborted');

CREATE TABLE ServiceRequest(
    id		                    INT NOT NULL UNIQUE AUTO_INCREMENT,
    service_request_key         CHAR(36) NOT NULL UNIQUE,
    service_id                  INT NOT NULL,
    service_request_status_id   INT NOT NULL,
    created_at                  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    CONSTRAINT fk_service_service_request FOREIGN KEY (service_id)
        REFERENCES Service(id),
    CONSTRAINT fk_service_request_status_service_request FOREIGN KEY (service_request_status_id)
        REFERENCES ServiceRequestStatus(id)
);   

CREATE TABLE ServiceRequestEvent(
    id                          INT NOT NULL UNIQUE AUTO_INCREMENT,
    service_request_id          INT  NOT NULL,
    service_request_status_id   INT NOT NULL,
    created_at                  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    CONSTRAINT fk_service_request_service_request_event FOREIGN KEY (service_requset_id)
        REFERENCES ServiceRequest(id),
    CONSTRAINT fk_service_request_status_event FOREIGN KEY (service_request_status_id)
        REFERENCES ServiceRequestStatus(id)
);
