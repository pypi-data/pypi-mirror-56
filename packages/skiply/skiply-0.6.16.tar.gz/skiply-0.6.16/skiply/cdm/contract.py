#!/usr/bin/python
# coding: utf8

# Copyright 2019 Skiply

from __future__ import unicode_literals


from .base import db_session, SkiplyBase

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from skiply.cdm import AssociationContractService


class Contract(SkiplyBase):
    ''' Device '''
    __tablename__ = 'so_contract'
    
    id = Column(Integer, primary_key=True, autoincrement=True)

    entity_id = Column('client_id', Integer, ForeignKey("so_client.id"), nullable=False)

    external_id = Column('external_id', String())

    contract_start_date = Column('start', DateTime())
    contract_end_date = Column('end', DateTime())

    contract_label = Column('description', String())

    services = relationship('Service', secondary=AssociationContractService)

    def __init__(self, entity_id, external_id, contract_start_date, contract_end_date, contract_label):
        self.entity_id = entity_id

        self.external_id = external_id

        self.contract_start_date = contract_start_date
        self.contract_end_date = contract_end_date

        self.contract_label = contract_label

    def __repr__(self):
        return '<Contract %r>' % (self.contract_label)

def get_contract(contract_id):
    session = db_session()
    try:
        results = session.query(Contract).filter(Contract.id == contract_id).first()
    except:
        print("DB Request get_contract(contract_id) Failed")
        results=None
    finally:
        session.close()

    return results

def get_contract(contract_id):
    session = db_session()
    try:
        results = session.query(Contract).filter(Contract.id == contract_id).first()
    except:
        print("DB Request get_contract(contract_id) Failed")
        results=None
    finally:
        session.close()

    return results
        