-- Table creation code
-- Note on foreign keys:
--   Many-to-one: the ONE side's primary key is stored as a foreign key in the MANY side

CREATE TABLE Region(
    region_id INT PRIMARY KEY,

    region_name VARCHAR(100),
    country VARCHAR(100)
);

CREATE TABLE GPUType(
    gpu_type_name VARCHAR(100) PRIMARY KEY
);

-- Inheritance:
-- SpecificGPUType is a subset of GPUType and stores extra GPU-specific information such as memory size
CREATE TABLE SpecificGPUType(
    -- PK and FK to represent inheritance relationship
    gpu_type_name VARCHAR(100) PRIMARY KEY,

    memory_gb INT,

    FOREIGN KEY(gpu_type_name) REFERENCES GPUType(gpu_type_name)
);

CREATE TABLE AIModel(
    model_id INT PRIMARY KEY,

    model_name VARCHAR(100)
);

CREATE TABLE GPUServer(
    machine_id VARCHAR(100) PRIMARY KEY,

    cpu_capacity INT,
    memory_capacity INT,
    gpu_capacity INT,

    region_id INT,
    gpu_type_name VARCHAR(100),
    FOREIGN KEY(region_id) REFERENCES Region(region_id),
    FOREIGN KEY(gpu_type_name) REFERENCES GPUType(gpu_type_name)
);

CREATE TABLE InferenceRequest(
    request_id INT PRIMARY KEY,

    submitted_at DOUBLE,
    input_size INT,
    status VARCHAR(100),
    response_time_ms DOUBLE,

    region_id INT,
    model_id INT,
    machine_id VARCHAR(100),
    FOREIGN KEY(region_id) REFERENCES Region(region_id),
    FOREIGN KEY(model_id) REFERENCES AIModel(model_id),
    FOREIGN KEY(machine_id) REFERENCES GPUServer(machine_id)
);

-- Weak entity:
-- MachineMetric uses the owner key and local metric_id as a composite primary key
CREATE TABLE MachineMetric(
    metric_id INT, -- local primary key

    start_time DOUBLE,
    end_time DOUBLE,
    worker_load DOUBLE,
    gpu_utilization DOUBLE,
    cpu_utilization DOUBLE,

    machine_id VARCHAR(100), -- FK and PK representing the owner relationship
    PRIMARY KEY(machine_id, metric_id),
    FOREIGN KEY(machine_id) REFERENCES GPUServer(machine_id)
);

-- Many-to-many relationship:
-- Both entity primary keys are stored here as foreign keys
-- The foreign keys then form the composite primary keys
CREATE TABLE Hosts(
    -- composite primary keys
    model_id INT,
    machine_id VARCHAR(100),
    PRIMARY KEY (model_id, machine_id),
    FOREIGN KEY(machine_id) REFERENCES GPUServer(machine_id),
    FOREIGN KEY(model_id) REFERENCES AIModel(model_id)
);

CREATE TABLE CompatibleWith(
    -- composite primary keys
    model_id INT,
    gpu_type_name VARCHAR(100),
    PRIMARY KEY(model_id, gpu_type_name),
    FOREIGN KEY(model_id) REFERENCES AIModel(model_id),
    FOREIGN KEY(gpu_type_name) REFERENCES GPUType(gpu_type_name)
);