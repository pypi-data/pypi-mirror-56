from featurize_jupyterlab.models import Experiment, Execution, Module
from featurize_jupyterlab.config import Config
from featurize_jupyterlab import core
from sqlalchemy.orm import sessionmaker
import pytest
import tornado
from featurize_jupyterlab.utils import create_session
from featurize_jupyterlab.handlers import setup_handlers
import json
# @pytest.fixture(scope='module')
# def setup_module(request):
#     def teardown_module():
#         print("teardown_module called.")
#     request.addfinalizer(teardown_module)
#     print('setup_module called.')

@pytest.fixture
def app():
    class NotebookApp:
        web_app = tornado.web.Application(base_url='/')
    setup_handlers(NotebookApp)
    return NotebookApp.web_app

# def test_1(setup_module):
#     print("test_1 beign")
#     session = sessionmaker(Config.engine)()

#     # experiment = Experiment(
#     #     name='ashe'
#     # )
#     # session.add(experiment)
#     # session.flush()
#     # print(experiment.id)
#     # execution = Execution(
#     #     task_type='train',
#     #     agent_config={},
#     #     experiment_id=experiment.id
#     # )
#     # # experiment.add_execution(execution)
#     # # module = {
#     # #     'name': 'test_module',
#     # #     'config': {}
#     # # }
#     # session.add(execution)
#     # session.commit()
#     # print(execution.experiment.id)
#     experiment = session.query(Experiment).filter(Experiment.name=='demo').first()
#     session.flush()
#     execution = session.query(Execution).filter(Execution.experiment_id==experiment.id).first()
#     response = await http_client.fetch(f'{base_url}/featurize/experiments/{experiment.id}/executions/{execution.id}/graph?graph_name=train_iteration_loss')
#     assert response.code == 200
#     result = json.loads(response.body)
#     print(result)
#     assert result['status'] == 'success'
#     print("test_1 end")


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