from data_factory import DataInfo
import os

if __name__ == '__main__':
    current_path = os.path.abspath(os.path.dirname(__file__))
    api_request_body_directory_path = os.path.join(current_path, 'api-request-body')
    random_test_data_directory_path = os.path.join(current_path, 'random-test-data')
    api_name = 'card-orders'
    # Todo 命名怪怪的
    dataInfo = DataInfo(api_name, {'testDataFile': random_test_data_directory_path,
                                   'sampleDataFile': api_request_body_directory_path})
    # 1.根据json文件创建csv文件，手动第三行 填写边界规则
    dataInfo.write_param_header_and_type()

    # 2.1穷举
    # dataInfo.generate_data_in_border_exhaustion()
    # 2.2批量生成
    dataInfo.generate_data_in_border_batch(1000)

    # 3.合并生产和 上面随机数据字段
    random_test_data_file_path = random_test_data_directory_path + '/card-orders' + '.csv'
    product_test_data_file_path = os.path.join(current_path, 'product-test-data', 'example.csv')
    DataInfo.merge_data_with_example_data(product_test_data_file_path, random_test_data_file_path)
