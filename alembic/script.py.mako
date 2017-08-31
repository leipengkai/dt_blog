# $ alembic revision -m "create account table" 创建一个基本数据库版本
# 创建之后 再编辑迁移脚本
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    ${upgrades if upgrades else "pass"}


def downgrade():
    ${downgrades if downgrades else "pass"}

# 执行迁移操作：
# $ alembic upgrade head
# $ alembic downgrade base 回退操作

# 对model/models的数据库进行修改之后 直接运行如下命令 即可更新数据库和此迁移脚本
# alembic revision --autogenerate -m "add weibo token fields for user"
