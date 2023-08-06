import pytest
import tornado
from featurize_jupyterlab.handlers import setup_handlers
from featurize_jupyterlab import core
from . import mock_components  # noqa: F401
from . import mock_user_data  # noqa: F401
import json
from featurize_jupyterlab.utils import create_session
from featurize_jupyterlab.models import Experiment, Execution, Module, Comment


@pytest.fixture
def app():
    class NotebookApp:
        web_app = tornado.web.Application(base_url='/')
    setup_handlers(NotebookApp)
    return NotebookApp.web_app


@pytest.mark.gen_test
async def test_get_all_components(http_client, base_url):
    session = create_session()
    experiment = session.query(Experiment).first()
    session.flush()
    response = await http_client.fetch(f'{base_url}/featurize/experiments/{experiment.id}/components')
    assert response.code == 200
    result = json.loads(response.body)
    assert result['status'] == 'success'
    assert len(result['data']) == len((core.registed_components()))


@pytest.mark.gen_test
async def test_get_all_experiments(http_client, base_url):
    response = await http_client.fetch(f'{base_url}/featurize/experiments')
    assert response.code == 200
    result = json.loads(response.body)
    print(f'test_get_all_experiments:{result}')
    assert result['status'] == 'success'


@pytest.mark.gen_test
async def test_add_one_experiment(http_client, base_url):
    data = {'name': 'test_add_experiment'}
    data_send = json.dumps(data)
    response = await http_client.fetch(f'{base_url}/featurize/experiments', method='POST', body=data_send)
    assert response.code == 200
    result = json.loads(response.body)
    assert result['status'] == 'success'


@pytest.mark.gen_test
async def test_get_one_experiment(http_client, base_url):
    session = create_session()
    experiment = session.query(Experiment).filter(Experiment.name == 'Mine Experiment').first()
    session.flush()
    response = await http_client.fetch(f'{base_url}/featurize/experiments/{experiment.id}')
    assert response.code == 200
    result = json.loads(response.body)
    print(f'test_get_one_experiments:{result}')
    assert result['status'] == 'success'


@pytest.mark.gen_test
async def test_update_one_experiment(http_client, base_url):
    session = create_session()
    experiment = session.query(Experiment).filter(Experiment.name == 'Mine Experiment2').first()
    session.flush()
    data = {'name':'2test_update_experiment',
            'enabled_packages':{'qqqdsd':'dsds'}}
    data_send = json.dumps(data)
    response = await http_client.fetch(f'{base_url}/featurize/experiments/{experiment.id}', method='PUT', body=data_send)
    assert response.code == 200
    result = json.loads(response.body)
    assert result['status'] == 'success'


@pytest.mark.gen_test
async def test_delete_one_experiment(http_client, base_url):
    session = create_session()
    experiment = session.query(Experiment).filter(Experiment.name=='Experiment For test_delete').first()
    session.flush()
    response = await http_client.fetch(f'{base_url}/featurize/experiments/{experiment.id}', method='DELETE')
    assert response.code == 200
    result = json.loads(response.body)
    assert result['status'] == 'success'


@pytest.mark.gen_test
async def test_get_all_executions(http_client, base_url):
    session = create_session()
    experiment = session.query(Experiment).first()
    session.flush()
    response = await http_client.fetch(f'{base_url}/featurize/experiments/{experiment.id}/executions')
    assert response.code == 200
    result = json.loads(response.body)
    print(f'test_get_all_executions:{result}')
    assert result['status'] == 'success'


@pytest.mark.gen_test
async def test_add_execution(http_client, base_url):
    session = create_session()
    experiment = session.query(Experiment).filter(Experiment.name=='Mine Experiment').first()
    session.flush()
    data = {'task_type': 'test_train2', 'agent_config':{}}
    data_send = json.dumps(data)
    response = await http_client.fetch(f'{base_url}/featurize/experiments/{experiment.id}/executions', method='POST', body=data_send)
    assert response.code == 200
    result = json.loads(response.body)
    print(result)
    assert result['status'] == 'success'


@pytest.mark.gen_test
async def test_delete_exection(http_client, base_url):
    session = create_session()
    experiment = session.query(Experiment).filter(Experiment.name=='Mine Experiment').first()
    session.flush()
    execution = Execution(status='not_running', task_type='train', experiment_id=experiment.id)
    session.add(execution)
    session.commit()
    response = await http_client.fetch(f'{base_url}/featurize/experiments/executions/{execution.id}')
    assert response.code == 200
    result = json.loads(response.body)
    print(result)
    assert result['status'] == 'success'


@pytest.mark.gen_test
async def test_update_exection(http_client, base_url):
    session = create_session()
    experiment = session.query(Experiment).filter(Experiment.name=='Mine Experiment').first()
    session.flush()
    execution = session.query(Execution).filter(Execution.experiment_id==experiment.id).first()
    session.flush()
    data = {'status':'running',
            'task_type': 'test_train3',
            'agent_config':
                    {'ashe':'zhunai',
                    'pb':'ppt'
                    }
            }
    data_send = json.dumps(data)
    response = await http_client.fetch(f'{base_url}/featurize/experiments/executions/{execution.id}', method='PUT', body=data_send)
    assert response.code == 200
    result = json.loads(response.body)
    print(result)
    assert result['status'] == 'success'


@pytest.mark.gen_test
async def test_get_all_modules(http_client, base_url):
    session = create_session()
    experiment = session.query(Experiment).filter(Experiment.name == 'Mine Experiment').first()
    session.flush()
    response = await http_client.fetch(f'{base_url}/featurize/experiments/{experiment.id}/modules')
    assert response.code == 200
    result = json.loads(response.body)
    print(f'test_get_all_modules:{result}')
    assert result['status'] == 'success'


@pytest.mark.gen_test
async def test_get_modules_of_execution(http_client, base_url):
    session = create_session()
    execution = session.query(Execution).first()
    session.flush()
    response = await http_client.fetch(f'{base_url}/featurize/executions/{execution.id}/modules')
    assert response.code == 200
    result = json.loads(response.body)
    assert result['status'] == 'success'


@pytest.mark.gen_test
async def test_add_one_module(http_client, base_url):
    session = create_session()
    experiment = session.query(Experiment).filter(Experiment.name=='Mine Experiment').first()
    session.flush()
    data = {'name':'test_add_module',
            'config':{'config_1':'123',
                    'config_2':'234'}
            }
    data_send = json.dumps(data)
    response = await http_client.fetch(f'{base_url}/featurize/experiments/{experiment.id}/modules', method='POST', body=data_send)
    assert response.code == 200
    result = json.loads(response.body)
    print(result)
    assert result['status'] == 'success'


@pytest.mark.gen_test
async def test_update_one_module(http_client, base_url):
    session = create_session()
    experiment = session.query(Experiment).filter(Experiment.name=='Mine Experiment').first()
    session.flush()
    module = session.query(Module).filter(Module.experiment_id==experiment.id).filter(Module.name=='Train DataLoader').first()
    session.flush()
    data = {'name':'test_update_module',
            'config':{'config_3':'123232',
                    'config_4':'23sds4'}
            }
    data_send = json.dumps(data)
    response = await http_client.fetch(f'{base_url}/featurize/experiments/modules/{module.id}', method='PUT', body=data_send)
    assert response.code == 200
    result = json.loads(response.body)
    print(result)
    assert result['status'] == 'success'


@pytest.mark.gen_test
async def test_delete_one_module(http_client, base_url):
    session = create_session()
    experiment = session.query(Experiment).filter(Experiment.name=='Mine Experiment').first()
    session.flush()
    module = Module(name='module_test_for_delete_module', experiment_id=experiment.id)
    session.add(module)
    session.commit()
    response = await http_client.fetch(f'{base_url}/featurize/experiments/modules/{module.id}', method='DELETE')
    assert response.code == 200
    result = json.loads(response.body)
    print(result)
    assert result['status'] == 'success'



@pytest.mark.gen_test
async def test_get_all_comments(http_client, base_url):
    session = create_session()
    experiment = session.query(Experiment).filter(Experiment.name=='Mine Experiment').first()
    session.flush()
    response = await http_client.fetch(f'{base_url}/featurize/comments/{experiment.id}')
    assert response.code == 200
    result = json.loads(response.body)
    print(result)
    assert result['status'] == 'success'



@pytest.mark.gen_test
async def test_add_one_comment(http_client, base_url):
    session = create_session()
    experiment = session.query(Experiment).filter(Experiment.name=='Mine Experiment3').first()
    session.flush()
    data = {'content':'test_add_comment',
            'commentable_type':'Experiment'
            }
    data_send = json.dumps(data)
    response = await http_client.fetch(f'{base_url}/featurize/comments/{experiment.id}', method='POST', body=data_send)
    assert response.code == 200
    result = json.loads(response.body)
    print(result)
    assert result['status'] == 'success'


@pytest.mark.gen_test
async def test_update_one_comment(http_client, base_url):
    session = create_session()
    experiment = session.query(Experiment).filter(Experiment.name=='Mine Experiment').first()
    session.flush()
    comment = session.query(Comment).filter(Comment.commentable_id==experiment.id).filter(Comment.content=='test comment 1').first()
    session.flush()
    data = {'content':'test_update_comment'}
    data_send = json.dumps(data)
    response = await http_client.fetch(f'{base_url}/featurize/comment/{comment.id}', method='PUT', body=data_send)
    assert response.code == 200
    result = json.loads(response.body)
    print(result)
    assert result['status'] == 'success'


@pytest.mark.gen_test
async def test_delete_one_comment(http_client, base_url):
    session = create_session()
    experiment = session.query(Experiment).filter(Experiment.name=='Mine Experiment').first()
    session.flush()
    comment = Comment(content='add for test delete comment ', commentable_id=experiment.id, commentable_type='Experiment')
    session.add(comment)
    session.commit()
    response = await http_client.fetch(f'{base_url}/featurize/comment/{comment.id}', method='DELETE')
    assert response.code == 200
    result = json.loads(response.body)
    print(result)
    assert result['status'] == 'success'


@pytest.mark.gen_test
async def test_get_all_graph(http_client, base_url):
    session = create_session()
    experiment = session.query(Experiment).filter(Experiment.name=='demo').first()
    session.flush()
    execution = session.query(Execution).filter(Execution.experiment_id==experiment.id).first()
    response = await http_client.fetch(f'{base_url}/featurize/executions/{execution.id}/graphs')
    assert response.code == 200
    result = json.loads(response.body)
    print(result)
    assert result['status'] == 'success'


@pytest.mark.gen_test
async def test_get_one_graph(http_client, base_url):
    session = create_session()
    experiment = session.query(Experiment).filter(Experiment.name=='demo').first()
    session.flush()
    execution = session.query(Execution).filter(Execution.experiment_id==experiment.id).first()
    response = await http_client.fetch(f'{base_url}/featurize/executions/{execution.id}/graph?graph_name=train_iteration_loss')
    assert response.code == 200
    result = json.loads(response.body)
    print(result)
    assert result['status'] == 'success'
